import uvicorn
from fastapi import FastAPI
from controllers.c_admin import admin_route
from controllers.c_employer import employer_router
from controllers.HistoryController import history_router, mqttApp

app = FastAPI()

mqttApp.init_app(app)

app.include_router(admin_route)
app.include_router(employer_router)
app.include_router(history_router)


@app.get('/')
def home():
    return "Hello Man"


# @app.post("/send_push_notification/")
# async def send_push_notification(device_token: str = Form(...), title: str = Form(...), message: str = Form(...)):
#     client = Client(app_id=ONESIGNAL_APP_ID, rest_api_key=ONESIGNAL_API_KEY)
#     notification_body = {
#         'contents': {'tr': 'Yeni bildirim', 'en': 'New notification'},
#         'included_segments': ['Active Users'],
#         'filters': [{'field': 'tag', 'key': 'level', 'relation': '>', 'value': 10}],
#     }
#     notification = client.send_notification(notification_body)
#
#     print(notification.status_code)
#     return {"message": "Push notification sent successfully"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, port=8089, host='0.0.0.0')
