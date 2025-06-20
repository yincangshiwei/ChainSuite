import tempfile
from concurrent.futures import wait
from pathlib import Path
from unittest.mock import patch

import pytest

import gradio as gr


def invalid_fn(message):
    return message


def double(message, history):
    return message + " " + message


async def async_greet(message, history):
    return "hi, " + message


def stream(message, history):
    for i in range(len(message)):
        yield message[: i + 1]


async def async_stream(message, history):
    for i in range(len(message)):
        yield message[: i + 1]


def count(message, history):
    return str(len(history))


def echo_system_prompt_plus_message(message, history, system_prompt, tokens):
    response = f"{system_prompt} {message}"
    for i in range(min(len(response), int(tokens))):
        yield response[: i + 1]


class TestInit:
    def test_no_fn(self):
        with pytest.raises(TypeError):
            gr.ChatInterface()  # type: ignore

    def test_configuring_buttons(self):
        chatbot = gr.ChatInterface(double, submit_btn=None, retry_btn=None)
        assert chatbot.submit_btn is None
        assert chatbot.retry_btn is None

    def test_concurrency_limit(self):
        chat = gr.ChatInterface(double, concurrency_limit=10)
        assert chat.concurrency_limit == 10
        fns = [
            fn
            for fn in chat.fns.values()
            if fn.name in {"_submit_fn", "_api_submit_fn"}
        ]
        assert all(fn.concurrency_limit == 10 for fn in fns)

    def test_custom_textbox(self):
        def chat():
            return "Hello"

        gr.ChatInterface(
            chat,
            chatbot=gr.Chatbot(height=400),
            textbox=gr.Textbox(placeholder="Type Message", container=False, scale=7),
            title="Test",
            clear_btn="Clear",
        )
        gr.ChatInterface(
            chat,
            chatbot=gr.Chatbot(height=400),
            textbox=gr.MultimodalTextbox(container=False, scale=7),
            title="Test",
            clear_btn="Clear",
        )

    def test_events_attached(self):
        chatbot = gr.ChatInterface(double)
        dependencies = chatbot.fns.values()
        textbox = chatbot.textbox._id
        assert chatbot.submit_btn
        submit_btn = chatbot.submit_btn._id
        assert next(
            (
                d
                for d in dependencies
                if d.targets == [(textbox, "submit"), (submit_btn, "click")]
            ),
            None,
        )
        assert chatbot.retry_btn and chatbot.clear_btn and chatbot.undo_btn
        for btn_id in [
            chatbot.retry_btn._id,
            chatbot.clear_btn._id,
            chatbot.undo_btn._id,
        ]:
            assert next(
                (d for d in dependencies if d.targets[0] == (btn_id, "click")),
                None,
            )

    def test_example_caching(self):
        with patch(
            "gradio.utils.get_cache_folder", return_value=Path(tempfile.mkdtemp())
        ):
            chatbot = gr.ChatInterface(
                double, examples=["hello", "hi"], cache_examples=True
            )
            prediction_hello = chatbot.examples_handler.load_from_cache(0)
            prediction_hi = chatbot.examples_handler.load_from_cache(1)
            assert prediction_hello[0].root[0] == ("hello", "hello hello")
            assert prediction_hi[0].root[0] == ("hi", "hi hi")

    @pytest.mark.asyncio
    async def test_example_caching_lazy(self):
        with patch(
            "gradio.utils.get_cache_folder", return_value=Path(tempfile.mkdtemp())
        ):
            chatbot = gr.ChatInterface(
                double, examples=["hello", "hi"], cache_examples="lazy"
            )
            async for _ in chatbot.examples_handler.async_lazy_cache(
                (0, ["hello"]), "hello"
            ):
                pass
            prediction_hello = chatbot.examples_handler.load_from_cache(0)
            assert prediction_hello[0].root[0] == ("hello", "hello hello")
            with pytest.raises(IndexError):
                prediction_hi = chatbot.examples_handler.load_from_cache(1)
                assert prediction_hi[0].root[0] == ("hi", "hi hi")

    def test_example_caching_async(self):
        with patch(
            "gradio.utils.get_cache_folder", return_value=Path(tempfile.mkdtemp())
        ):
            chatbot = gr.ChatInterface(
                async_greet, examples=["abubakar", "tom"], cache_examples=True
            )
            prediction_hello = chatbot.examples_handler.load_from_cache(0)
            prediction_hi = chatbot.examples_handler.load_from_cache(1)
            assert prediction_hello[0].root[0] == ("abubakar", "hi, abubakar")
            assert prediction_hi[0].root[0] == ("tom", "hi, tom")

    def test_example_caching_with_streaming(self):
        with patch(
            "gradio.utils.get_cache_folder", return_value=Path(tempfile.mkdtemp())
        ):
            chatbot = gr.ChatInterface(
                stream, examples=["hello", "hi"], cache_examples=True
            )
            prediction_hello = chatbot.examples_handler.load_from_cache(0)
            prediction_hi = chatbot.examples_handler.load_from_cache(1)
            assert prediction_hello[0].root[0] == ("hello", "hello")
            assert prediction_hi[0].root[0] == ("hi", "hi")

    def test_example_caching_with_streaming_async(self):
        with patch(
            "gradio.utils.get_cache_folder", return_value=Path(tempfile.mkdtemp())
        ):
            chatbot = gr.ChatInterface(
                async_stream, examples=["hello", "hi"], cache_examples=True
            )
            prediction_hello = chatbot.examples_handler.load_from_cache(0)
            prediction_hi = chatbot.examples_handler.load_from_cache(1)
            assert prediction_hello[0].root[0] == ("hello", "hello")
            assert prediction_hi[0].root[0] == ("hi", "hi")

    def test_default_accordion_params(self):
        chatbot = gr.ChatInterface(
            echo_system_prompt_plus_message,
            additional_inputs=["textbox", "slider"],
        )
        accordion = [
            comp
            for comp in chatbot.blocks.values()
            if comp.get_config().get("name") == "accordion"
        ][0]
        assert accordion.get_config().get("open") is False
        assert accordion.get_config().get("label") == "Additional Inputs"

    def test_setting_accordion_params(self, monkeypatch):
        chatbot = gr.ChatInterface(
            echo_system_prompt_plus_message,
            additional_inputs=["textbox", "slider"],
            additional_inputs_accordion=gr.Accordion(open=True, label="MOAR"),
        )
        accordion = [
            comp
            for comp in chatbot.blocks.values()
            if comp.get_config().get("name") == "accordion"
        ][0]
        assert accordion.get_config().get("open") is True
        assert accordion.get_config().get("label") == "MOAR"

    def test_example_caching_with_additional_inputs(self, monkeypatch):
        with patch(
            "gradio.utils.get_cache_folder", return_value=Path(tempfile.mkdtemp())
        ):
            chatbot = gr.ChatInterface(
                echo_system_prompt_plus_message,
                additional_inputs=["textbox", "slider"],
                examples=[["hello", "robot", 100], ["hi", "robot", 2]],
                cache_examples=True,
            )
            prediction_hello = chatbot.examples_handler.load_from_cache(0)
            prediction_hi = chatbot.examples_handler.load_from_cache(1)
            assert prediction_hello[0].root[0] == ("hello", "robot hello")
            assert prediction_hi[0].root[0] == ("hi", "ro")

    def test_example_caching_with_additional_inputs_already_rendered(self, monkeypatch):
        with patch(
            "gradio.utils.get_cache_folder", return_value=Path(tempfile.mkdtemp())
        ):
            with gr.Blocks():
                with gr.Accordion("Inputs"):
                    text = gr.Textbox()
                    slider = gr.Slider()
                    chatbot = gr.ChatInterface(
                        echo_system_prompt_plus_message,
                        additional_inputs=[text, slider],
                        examples=[["hello", "robot", 100], ["hi", "robot", 2]],
                        cache_examples=True,
                    )
            prediction_hello = chatbot.examples_handler.load_from_cache(0)
            prediction_hi = chatbot.examples_handler.load_from_cache(1)
            assert prediction_hello[0].root[0] == ("hello", "robot hello")
            assert prediction_hi[0].root[0] == ("hi", "ro")

    def test_custom_chatbot_with_events(self):
        with gr.Blocks() as demo:
            chatbot = gr.Chatbot()
            chatbot.like(lambda: None, None, None)
            gr.ChatInterface(fn=lambda x, y: x, chatbot=chatbot)
        dependencies = demo.fns.values()
        assert next(
            (d for d in dependencies if d.targets == [(chatbot._id, "like")]),
            None,
        )


class TestAPI:
    def test_get_api_info(self):
        chatbot = gr.ChatInterface(double)
        api_info = chatbot.get_api_info()
        assert api_info
        assert len(api_info["named_endpoints"]) == 1
        assert len(api_info["unnamed_endpoints"]) == 0
        assert "/chat" in api_info["named_endpoints"]

    @pytest.mark.parametrize("type", ["tuples", "messages"])
    def test_streaming_api(self, type, connect):
        chatbot = gr.ChatInterface(stream, type=type).queue()
        with connect(chatbot) as client:
            job = client.submit("hello")
            wait([job])
            assert job.outputs() == ["h", "he", "hel", "hell", "hello"]

    @pytest.mark.parametrize("type", ["tuples", "messages"])
    def test_streaming_api_async(self, type, connect):
        chatbot = gr.ChatInterface(async_stream, type=type).queue()
        with connect(chatbot) as client:
            job = client.submit("hello")
            wait([job])
            assert job.outputs() == ["h", "he", "hel", "hell", "hello"]

    @pytest.mark.parametrize("type", ["tuples", "messages"])
    def test_non_streaming_api(self, type, connect):
        chatbot = gr.ChatInterface(double, type=type)
        with connect(chatbot) as client:
            result = client.predict("hello")
            assert result == "hello hello"

    @pytest.mark.parametrize("type", ["tuples", "messages"])
    def test_non_streaming_api_async(self, type, connect):
        chatbot = gr.ChatInterface(async_greet, type=type)
        with connect(chatbot) as client:
            result = client.predict("gradio")
            assert result == "hi, gradio"

    @pytest.mark.parametrize("type", ["tuples", "messages"])
    def test_streaming_api_with_additional_inputs(self, type, connect):
        chatbot = gr.ChatInterface(
            echo_system_prompt_plus_message,
            type=type,
            additional_inputs=["textbox", "slider"],
        ).queue()
        with connect(chatbot) as client:
            job = client.submit("hello", "robot", 7)
            wait([job])
            assert job.outputs() == [
                "r",
                "ro",
                "rob",
                "robo",
                "robot",
                "robot ",
                "robot h",
            ]

    @pytest.mark.parametrize("type", ["tuples", "messages"])
    def test_multimodal_api(self, type, connect):
        def double_multimodal(msg, history):
            return msg["text"] + " " + msg["text"]

        chatbot = gr.ChatInterface(
            double_multimodal,
            type=type,
            multimodal=True,
        )
        with connect(chatbot) as client:
            result = client.predict({"text": "hello", "files": []}, api_name="/chat")
            assert result == "hello hello"
