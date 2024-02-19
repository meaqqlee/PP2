# Поскольку задание включает работу с файлом JSON, который непосредственно не предоставлен,
# я создам пример данных JSON в соответствии с описанием задачи и произведу его разбор.

# Пример данных JSON
json_data = """
{
  "imdata": [
    {
      "l1PhysIf": {
        "attributes": {
          "dn": "topology/pod-1/node-201/sys/phys-[eth1/33]",
          "descr": "",
          "speed": "inherit",
          "mtu": "9150"
        }
      }
    },
    {
      "l1PhysIf": {
        "attributes": {
          "dn": "topology/pod-1/node-201/sys/phys-[eth1/34]",
          "descr": "",
          "speed": "inherit",
          "mtu": "9150"
        }
      }
    },
    {
      "l1PhysIf": {
        "attributes": {
          "dn": "topology/pod-1/node-201/sys/phys-[eth1/35]",
          "descr": "",
          "speed": "inherit",
          "mtu": "9150"
        }
      }
    }
  ]
}
"""

# Импортируем модуль для работы с JSON
import json

# Преобразуем строку JSON в объект Python
data = json.loads(json_data)

# Выводим заголовок таблицы
print("Interface Status")
print("="*80)
print("{:<50} {:<20} {:<8} {:<6}".format("DN", "Description", "Speed", "MTU"))

# Выводим данные из JSON
for item in data["imdata"]:
    dn = item["l1PhysIf"]["attributes"]["dn"]
    descr = item["l1PhysIf"]["attributes"].get("descr", "")  # Используем метод get для обработки отсутствующих описаний
    speed = item["l1PhysIf"]["attributes"]["speed"]
    mtu = item["l1PhysIf"]["attributes"]["mtu"]
    print("{:<50} {:<20} {:<8} {:<6}".format(dn, descr, speed, mtu))