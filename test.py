from modules.HomeAssistant import HomeAssistant

home_assistant = HomeAssistant()
response = home_assistant.get_info("")
print(response.text)
