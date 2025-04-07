from agent import agent
from pydantic_ai import BinaryContent
import httpx
from pydantic_ai.models.gemini import GeminiModelSettings
from pydantic_ai import UnexpectedModelBehavior


def test_agent_exists():
    try:
        result = agent.run_sync('Where does "hello world" come from?')
        print(result)
    except Exception as e:
        print(f"Agent does not exist: {e}")


def test_geo_guessing_from_web_image():
    image_response = httpx.get("https://iili.io/3Hs4FMg.png")  # Pydantic logo
    try:
        result = agent.run_sync(
            [
                "What company is this logo from?",
                BinaryContent(data=image_response.content, media_type="image/png"),
            ],
            model_settings=GeminiModelSettings(
                temperature=0.1,
                top_p=0.5,
                max_output_tokens=4096,
                response_modalities=["TEXT"],
                gemini_safety_settings=[
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "OFF",
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "OFF",
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "OFF",
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "OFF",
                    },
                ],
            ),
        )
        print(result.data)
    except UnexpectedModelBehavior as e:
        print(e)
        """
        Safety settings triggered, body:
        <safety settings details>
        """

    assert "Pydantic" in result.data
