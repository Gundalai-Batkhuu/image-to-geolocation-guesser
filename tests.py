from agent import agent
from pydantic_ai import BinaryContent
import httpx

def test_agent_exists():
    try:
        result = agent.run_sync('Where does "hello world" come from?')
        print(result)
    except Exception as e:
        print(f"Agent does not exist: {e}")

def test_agent_settings_exist():
    settings = agent.model_settings
    print(settings)
    assert settings

def test_geo_guessing():
    image_response = httpx.get('https://iili.io/3Hs4FMg.png')  # Pydantic logo

    result = agent.run_sync(
        [
            'What company is this logo from?',
            BinaryContent(data=image_response.content, media_type='image/png'),
        ]
    )
    print(result.data)
    assert "Pydantic" in result.data



