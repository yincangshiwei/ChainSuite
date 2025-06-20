from __future__ import annotations

import json
import os
import sys
import warnings
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from typing_extensions import Literal

from gradio import EventData, Request
from gradio.external_utils import format_ner_list
from gradio.utils import (
    FileSize,
    UnhashableKeyDict,
    _parse_file_size,
    abspath,
    append_unique_suffix,
    assert_configs_are_equivalent_besides_ids,
    check_function_inputs_match,
    colab_check,
    delete_none,
    diff,
    download_if_url,
    get_extension_from_file_path_or_url,
    get_function_params,
    get_type_hints,
    ipython_check,
    is_in_or_equal,
    is_special_typed_parameter,
    kaggle_check,
    sagemaker_check,
    sanitize_list_for_csv,
    sanitize_value_for_csv,
    tex2svg,
    validate_url,
)

os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"


class TestUtils:
    @patch("IPython.get_ipython")
    def test_colab_check_no_ipython(self, mock_get_ipython):
        mock_get_ipython.return_value = None
        assert colab_check() is False

    @patch("IPython.get_ipython")
    def test_ipython_check_import_fail(self, mock_get_ipython):
        mock_get_ipython.side_effect = ImportError()
        assert ipython_check() is False

    @patch("IPython.get_ipython")
    def test_ipython_check_no_ipython(self, mock_get_ipython):
        mock_get_ipython.return_value = None
        assert ipython_check() is False

    def test_download_if_url_doesnt_crash_on_connection_error(self):
        in_article = "placeholder"
        out_article = download_if_url(in_article)
        assert out_article == in_article

        # non-printable characters are not allowed in URL address
        in_article = "text\twith\rnon-printable\nASCII\x00characters"
        out_article = download_if_url(in_article)
        assert out_article == in_article

        # only files with HTTP(S) URL can be downloaded
        in_article = "ftp://localhost/tmp/index.html"
        out_article = download_if_url(in_article)
        assert out_article == in_article

        in_article = "file:///C:/tmp/index.html"
        out_article = download_if_url(in_article)
        assert out_article == in_article

        # this address will raise ValueError during parsing
        in_article = "https://[unmatched_bracket#?:@/index.html"
        out_article = download_if_url(in_article)
        assert out_article == in_article

    def test_download_if_url_correct_parse(self):
        in_article = "https://github.com/gradio-app/gradio/blob/master/README.md"
        out_article = download_if_url(in_article)
        assert out_article != in_article

    def test_sagemaker_check_false(self):
        assert not sagemaker_check()

    def test_sagemaker_check_false_if_boto3_not_installed(self):
        with patch.dict(sys.modules, {"boto3": None}, clear=True):
            assert not sagemaker_check()

    @patch("boto3.session.Session.client")
    def test_sagemaker_check_true(self, mock_client):
        mock_client().get_caller_identity = MagicMock(
            return_value={
                "Arn": "arn:aws:sts::67364438:assumed-role/SageMaker-Datascients/SageMaker"
            }
        )
        assert sagemaker_check()

    def test_kaggle_check_false(self):
        assert not kaggle_check()

    def test_kaggle_check_true_when_run_type_set(self):
        with patch.dict(
            os.environ, {"KAGGLE_KERNEL_RUN_TYPE": "Interactive"}, clear=True
        ):
            assert kaggle_check()

    def test_kaggle_check_true_when_both_set(self):
        with patch.dict(
            os.environ,
            {"KAGGLE_KERNEL_RUN_TYPE": "Interactive", "GFOOTBALL_DATA_DIR": "./"},
            clear=True,
        ):
            assert kaggle_check()

    def test_kaggle_check_false_when_neither_set(self):
        with patch.dict(
            os.environ,
            {"KAGGLE_KERNEL_RUN_TYPE": "", "GFOOTBALL_DATA_DIR": ""},
            clear=True,
        ):
            assert not kaggle_check()


def test_assert_configs_are_equivalent():
    test_dir = Path(__file__).parent / "test_files"
    with open(test_dir / "xray_config.json") as fp:
        xray_config = json.load(fp)
    with open(test_dir / "xray_config_diff_ids.json") as fp:
        xray_config_diff_ids = json.load(fp)
    with open(test_dir / "xray_config_wrong.json") as fp:
        xray_config_wrong = json.load(fp)

    assert assert_configs_are_equivalent_besides_ids(xray_config, xray_config)
    assert assert_configs_are_equivalent_besides_ids(xray_config, xray_config_diff_ids)
    with pytest.raises(ValueError):
        assert_configs_are_equivalent_besides_ids(xray_config, xray_config_wrong)


class TestFormatNERList:
    def test_format_ner_list_standard(self):
        string = "Wolfgang lives in Berlin"
        groups = [
            {"entity_group": "PER", "start": 0, "end": 8},
            {"entity_group": "LOC", "start": 18, "end": 24},
        ]
        result = [
            ("", None),
            ("Wolfgang", "PER"),
            (" lives in ", None),
            ("Berlin", "LOC"),
            ("", None),
        ]
        assert format_ner_list(string, groups) == result

    def test_format_ner_list_empty(self):
        string = "I live in a city"
        groups = []
        result = [("I live in a city", None)]
        assert format_ner_list(string, groups) == result


class TestDeleteNone:
    """Credit: https://stackoverflow.com/questions/33797126/proper-way-to-remove-keys-in-dictionary-with-none-values-in-python"""

    def test_delete_none(self):
        input = {
            "a": 12,
            "b": 34,
            "c": None,
            "k": {
                "d": 34,
                "t": None,
                "m": [{"k": 23, "t": None}, [None, 1, 2, 3], {1, 2, None}],
                None: 123,
            },
        }
        truth = {
            "a": 12,
            "b": 34,
            "k": {
                "d": 34,
                "t": None,
                "m": [{"k": 23, "t": None}, [None, 1, 2, 3], {1, 2, None}],
                None: 123,
            },
        }
        assert delete_none(input) == truth


class TestSanitizeForCSV:
    def test_unsafe_value(self):
        assert sanitize_value_for_csv("=OPEN()") == "'=OPEN()"
        assert sanitize_value_for_csv("=1+2") == "'=1+2"
        assert sanitize_value_for_csv('=1+2";=1+2') == "'=1+2\";=1+2"

    def test_safe_value(self):
        assert sanitize_value_for_csv(4) == 4
        assert sanitize_value_for_csv(-44.44) == -44.44
        assert sanitize_value_for_csv("1+1=2") == "1+1=2"
        assert sanitize_value_for_csv("1aaa2") == "1aaa2"

    def test_list(self):
        assert sanitize_list_for_csv([4, "def=", "=gh+ij"]) == [4, "def=", "'=gh+ij"]
        assert sanitize_list_for_csv(
            [["=abc", "def", "gh,+ij"], ["abc", "=def", "+ghij"]]
        ) == [["'=abc", "def", "'gh,+ij"], ["abc", "'=def", "'+ghij"]]
        assert sanitize_list_for_csv([1, ["ab", "=de"]]) == [1, ["ab", "'=de"]]


class TestValidateURL:
    @pytest.mark.flaky
    def test_valid_urls(self):
        assert validate_url("https://www.gradio.app")
        assert validate_url("http://gradio.dev")
        assert validate_url(
            "https://upload.wikimedia.org/wikipedia/commons/b/b0/Bengal_tiger_%28Panthera_tigris_tigris%29_female_3_crop.jpg"
        )
        assert validate_url(
            "https://huggingface.co/datasets/Xenova/transformers.js-docs/resolve/main/bread_small.png"
        )

    def test_invalid_urls(self):
        assert not (validate_url("C:/Users/"))
        assert not (validate_url("C:\\Users\\"))
        assert not (validate_url("/home/user"))


class TestAppendUniqueSuffix:
    def test_no_suffix(self):
        name = "test"
        list_of_names = ["test_1", "test_2"]
        assert append_unique_suffix(name, list_of_names) == name

    def test_first_suffix(self):
        name = "test"
        list_of_names = ["test", "test_-1"]
        assert append_unique_suffix(name, list_of_names) == "test_1"

    def test_later_suffix(self):
        name = "test"
        list_of_names = ["test", "test_1", "test_2", "test_3"]
        assert append_unique_suffix(name, list_of_names) == "test_4"


class TestAbspath:
    def test_abspath_no_symlink(self):
        resolved_path = str(abspath("../gradio/gradio/test_data/lion.jpg"))
        assert ".." not in resolved_path

    @pytest.mark.skipif(
        sys.platform.startswith("win"),
        reason="Windows doesn't allow creation of sym links without administrative privileges",
    )
    def test_abspath_symlink_path(self):
        os.symlink("gradio/test_data", "gradio/test_link", True)
        resolved_path = str(abspath("../gradio/gradio/test_link/lion.jpg"))
        os.unlink("gradio/test_link")
        assert "test_link" in resolved_path

    @pytest.mark.skipif(
        sys.platform.startswith("win"),
        reason="Windows doesn't allow creation of sym links without administrative privileges",
    )
    def test_abspath_symlink_dir(self):
        os.symlink("gradio/test_data", "gradio/test_link", True)
        full_path = os.path.join(os.getcwd(), "gradio/test_link/lion.jpg")
        resolved_path = str(abspath(full_path))
        os.unlink("gradio/test_link")
        assert "test_link" in resolved_path
        assert full_path == resolved_path


class TestGetTypeHints:
    def test_get_type_hints(self):
        class F:
            def __call__(self, s: str):
                return s

        class C:
            def f(self, s: str):
                return s

        def f(s: str):
            return s

        class GenericObject:
            pass

        test_objs = [F(), C().f, f]

        for x in test_objs:
            hints = get_type_hints(x)
            assert len(hints) == 1
            assert hints["s"] == str

        assert len(get_type_hints(GenericObject())) == 0

    def test_is_special_typed_parameter(self):
        def func(a: list[str], b: Literal["a", "b"], c, d: Request, e: Request | None):
            pass

        hints = get_type_hints(func)
        assert not is_special_typed_parameter("a", hints)
        assert not is_special_typed_parameter("b", hints)
        assert not is_special_typed_parameter("c", hints)
        assert is_special_typed_parameter("d", hints)
        assert is_special_typed_parameter("e", hints)

    def test_is_special_typed_parameter_with_pipe(self):
        def func(a: Request, b: str | int, c: list[str]):
            pass

        hints = get_type_hints(func)
        assert is_special_typed_parameter("a", hints)
        assert not is_special_typed_parameter("b", hints)
        assert not is_special_typed_parameter("c", hints)


class TestCheckFunctionInputsMatch:
    def test_check_function_inputs_match(self):
        class F:
            def __call__(self, s: str, evt: EventData):
                return s

        class C:
            def f(self, s: str, evt: EventData):
                return s

        def f(s: str, evt: EventData):
            return s

        test_objs = [F(), C().f, f]

        with warnings.catch_warnings():
            warnings.simplefilter("error")  # Ensure there're no warnings raised here.

            for x in test_objs:
                check_function_inputs_match(x, [None], False)


def test_tex2svg_preserves_matplotlib_backend():
    import matplotlib

    matplotlib.use("svg")
    tex2svg("1+1=2")
    assert matplotlib.get_backend() == "svg"
    with pytest.raises(
        Exception  # specifically a pyparsing.ParseException but not important here
    ):
        tex2svg("$$$1+1=2$$$")
    assert matplotlib.get_backend() == "svg"


def test_is_in_or_equal():
    assert is_in_or_equal("files/lion.jpg", "files/lion.jpg")
    assert is_in_or_equal("files/lion.jpg", "files")
    assert is_in_or_equal("files/lion.._M.jpg", "files")
    assert not is_in_or_equal("files", "files/lion.jpg")
    assert is_in_or_equal("/home/usr/notes.txt", "/home/usr/")
    assert not is_in_or_equal("/home/usr/subdirectory", "/home/usr/notes.txt")
    assert not is_in_or_equal("/home/usr/../../etc/notes.txt", "/home/usr/")
    assert not is_in_or_equal("/safe_dir/subdir/../../unsafe_file.txt", "/safe_dir/")


def create_path_string():
    return st.lists(
        st.one_of(
            st.text(
                alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-",
                min_size=1,
            ),
            st.just(".."),
            st.just("."),
        ),
        min_size=1,
        max_size=10,  # Limit depth to avoid excessively long paths
    ).map(lambda x: os.path.join(*x))


def my_check(path_1, path_2):
    try:
        path_1 = Path(path_1).resolve()
        path_2 = Path(path_2).resolve()
        _ = path_1.relative_to(path_2)
        return True
    except ValueError:
        return False


@settings(derandomize=os.getenv("CI") is not None)
@given(
    path_1=create_path_string(),
    path_2=create_path_string(),
)
def test_is_in_or_equal_fuzzer(path_1, path_2):
    try:
        # Convert to absolute paths
        abs_path_1 = abspath(path_1)
        abs_path_2 = abspath(path_2)
        result = is_in_or_equal(abs_path_1, abs_path_2)
        assert result == my_check(abs_path_1, abs_path_2)

    except Exception as e:
        pytest.fail(f"Exception raised: {e}")


# Additional test for known edge cases
@pytest.mark.parametrize(
    "path_1,path_2,expected",
    [
        ("/AAA/a/../a", "/AAA", True),
        ("//AA/a", "/tmp", False),
        ("/AAA/..", "/AAA", False),
        ("/a/b/c", "/d/e/f", False),
        (".", "..", True),
        ("..", ".", False),
        ("/a/b/./c", "/a/b", True),
        ("/a/b/../c", "/a", True),
        ("/a/b/c", "/a/b/c/../d", False),
        ("/", "/a", False),
        ("/a", "/", True),
    ],
)
def test_is_in_or_equal_edge_cases(path_1, path_2, expected):
    assert is_in_or_equal(path_1, path_2) == expected


@pytest.mark.parametrize(
    "path_or_url, extension",
    [
        ("https://example.com/avatar/xxxx.mp4?se=2023-11-16T06:51:23Z&sp=r", "mp4"),
        ("/home/user/documents/example.pdf", "pdf"),
        ("C:\\Users\\user\\documents\\example.png", "png"),
        ("C:/Users/user/documents/example", ""),
    ],
)
def test_get_extension_from_file_path_or_url(path_or_url, extension):
    assert get_extension_from_file_path_or_url(path_or_url) == extension


@pytest.mark.parametrize(
    "old, new, expected_diff",
    [
        ({"a": 1, "b": 2}, {"a": 1, "b": 2}, []),
        ({}, {"a": 1, "b": 2}, [("add", ["a"], 1), ("add", ["b"], 2)]),
        (["a", "b"], {"a": 1, "b": 2}, [("replace", [], {"a": 1, "b": 2})]),
        ("abc", "abcdef", [("append", [], "def")]),
    ],
)
def test_diff(old, new, expected_diff):
    assert diff(old, new) == expected_diff


class TestFunctionParams:
    def test_regular_function(self):
        def func(a, b=10, c="default", d=None):
            pass

        assert get_function_params(func) == [
            ("a", False, None),
            ("b", True, 10),
            ("c", True, "default"),
            ("d", True, None),
        ]

    def test_function_no_params(self):
        def func():
            pass

        assert get_function_params(func) == []

    def test_lambda_function(self):
        assert get_function_params(lambda x, y: x + y) == [
            ("x", False, None),
            ("y", False, None),
        ]

    def test_function_with_args(self):
        def func(a, *args):
            pass

        assert get_function_params(func) == [("a", False, None)]

    def test_function_with_kwargs(self):
        def func(a, **kwargs):
            pass

        assert get_function_params(func) == [("a", False, None)]

    def test_function_with_special_args(self):
        def func(a, r: Request, b=10):
            pass

        assert get_function_params(func) == [("a", False, None), ("b", True, 10)]

        def func2(a, r: Request | None = None, b="abc"):
            pass

        assert get_function_params(func2) == [("a", False, None), ("b", True, "abc")]

    def test_class_method_skip_first_param(self):
        class MyClass:
            def method(self, arg1, arg2=42):
                pass

        assert get_function_params(MyClass().method) == [
            ("arg1", False, None),
            ("arg2", True, 42),
        ]

    def test_static_method_no_skip(self):
        class MyClass:
            @staticmethod
            def method(arg1, arg2=42):
                pass

        assert get_function_params(MyClass.method) == [
            ("arg1", False, None),
            ("arg2", True, 42),
        ]

    def test_class_method_with_args(self):
        class MyClass:
            def method(self, a, *args, b=42):
                pass

        assert get_function_params(MyClass().method) == [("a", False, None)]

    def test_lambda_with_args(self):
        assert get_function_params(lambda x, *args: x) == [("x", False, None)]

    def test_lambda_with_kwargs(self):
        assert get_function_params(lambda x, **kwargs: x) == [("x", False, None)]


def test_parse_file_size():
    assert _parse_file_size("1kb") == 1 * FileSize.KB
    assert _parse_file_size("1mb") == 1 * FileSize.MB
    assert _parse_file_size("505 Mb") == 505 * FileSize.MB


class TestUnhashableKeyDict:
    def test_set_get_simple(self):
        d = UnhashableKeyDict()
        d["a"] = 1
        assert d["a"] == 1

    def test_set_get_unhashable(self):
        d = UnhashableKeyDict()
        key = [1, 2, 3]
        key2 = [1, 2, 3]
        d[key] = "value"
        assert d[key] == "value"
        assert d[key2] == "value"

    def test_set_get_numpy_array(self):
        d = UnhashableKeyDict()
        key = np.array([1, 2, 3])
        key2 = np.array([1, 2, 3])
        d[key] = "numpy value"
        assert d[key2] == "numpy value"

    def test_overwrite(self):
        d = UnhashableKeyDict()
        d["key"] = "old"
        d["key"] = "new"
        assert d["key"] == "new"

    def test_delete(self):
        d = UnhashableKeyDict()
        d["key"] = "value"
        del d["key"]
        assert len(d) == 0
        with pytest.raises(KeyError):
            d["key"]

    def test_delete_nonexistent(self):
        d = UnhashableKeyDict()
        with pytest.raises(KeyError):
            del d["nonexistent"]

    def test_len(self):
        d = UnhashableKeyDict()
        assert len(d) == 0
        d["a"] = 1
        d["b"] = 2
        assert len(d) == 2

    def test_contains(self):
        d = UnhashableKeyDict()
        d["key"] = "value"
        assert "key" in d
        assert "nonexistent" not in d

    def test_get_nonexistent(self):
        d = UnhashableKeyDict()
        with pytest.raises(KeyError):
            d["nonexistent"]
