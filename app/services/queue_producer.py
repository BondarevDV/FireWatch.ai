# Расположение: /fire_detection_api/app/services/queue_producer.py

import time

class QueueProducer:
    def send_notification(self, message: dict):
        print(f"\n--- [BACKGROUND TASK 2] ---")
        print("Имитация отправки уведомления в очередь (e.g., RabbitMQ)...")
        time.sleep(1)
        print(f"Сообщение отправлено: {message}")
        print(f"--- [BACKGROUND TASK 2 FINISHED] ---\n")

# Зависимость для DI
queue_producer_instance = QueueProducer()
def get_queue_producer() -> QueueProducer:
    return queue_producer_instance