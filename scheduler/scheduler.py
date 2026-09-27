import os, shutil, logging, time, schedule

# Настройка журнала
logging.basicConfig(filename="scheduler.log", level=logging.INFO, format="%(asctime)s - %(message)s", encoding="utf-8")
tasks = []

# Выполнение операций над файлами
def run_op(op, src, dst):
    try:
        if op == 'copy': shutil.copy(src, dst)
        elif op == 'move': shutil.move(src, dst)
        elif op == 'delete': os.remove(src)
        elif op == 'archive': shutil.make_archive(dst, 'zip', src)
        msg = f"УСПЕХ: {op} ({src})"
    except Exception as e:
        msg = f"ОШИБКА: {op} ({src}) -> {e}"
    print(msg)
    logging.info(msg)

# Главный цикл
while True:
    cmd = input("\n[1]Добавить [2]Просмотр [3]Удалить [4]Запустить [5]Выход: ").strip()
    
    if cmd == '1': # Добавление
        op = input("Операция (copy/move/delete/archive): ").strip()
        src = input("Исходный файл: ").strip()
        dst = input("Назначение (Enter если не нужно): ").strip() or None
        tm = input("Время (пример 11:11): ").strip()
        tasks.append({'op': op, 'src': src, 'dst': dst, 'time': tm})
        logging.info(f"задача добавлена: {op} {src} на {tm}")

    elif cmd == '2': # Просмотр
        for i, t in enumerate(tasks, 1):
            print(f"{i}. {t['op']} | {t['src']} -> {t['dst']} | {t['time']}")

    elif cmd == '3': # Удаление
        idx = int(input("Номер задачи: ")) - 1
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            logging.info(f"ЗАДАЧА УДАЛЕНА: {removed['op']}")

    elif cmd == '4': # Запуск
        if not tasks: continue
        schedule.clear()
        for t in tasks:
            schedule.every().day.at(t['time']).do(run_op, t['op'], t['src'], t['dst'])
        print("Шедулер запущен (Ctrl+C для остановки)...")
        try:
            while True: schedule.run_pending(); time.sleep(1)
        except KeyboardInterrupt: pass

    elif cmd == '5': break