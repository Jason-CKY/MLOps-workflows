from locust import HttpUser, task, between

class HelloWorldUser(HttpUser):
    wait_time = between(0.5, 500)

    @task
    def predict(self):
        with open('doge.jpg', 'rb') as image:
            self.client.post('/predict', files={'img_file': image})

