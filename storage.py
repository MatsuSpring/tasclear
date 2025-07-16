import flet as ft

# Client Storage Keys
LESSONS_KEY = 'lessons_data'
TASKS_KEY = 'tasks_data'
NEXT_LESSON_ID_KEY = 'next_lesson_id'
NEXT_TASK_ID_KEY = 'next_task_id'

def _get_next_id(page: ft.Page, key: str) -> int:
    current_id = page.client_storage.get(key)
    if current_id is None:
        current_id = 1
    else:
        current_id += 1
    page.client_storage.set(key, current_id)
    return current_id

def init_storage(page: ft.Page):
    if not page.client_storage.contains_key(LESSONS_KEY):
        page.client_storage.set(LESSONS_KEY, {})
        page.client_storage.set(NEXT_LESSON_ID_KEY, 1)
    if not page.client_storage.contains_key(TASKS_KEY):
        page.client_storage.set(TASKS_KEY, {})
        page.client_storage.set(NEXT_TASK_ID_KEY, 1)

def get_lesson_name(page: ft.Page, lesson_id: int) -> str:
    lessons = page.client_storage.get(LESSONS_KEY)
    return lessons.get(str(lesson_id), {}).get('lesson_name', 'Unknown Lesson')

def get_tasks_by_lesson(page: ft.Page, lesson_id: int) -> list:
    all_tasks = page.client_storage.get(TASKS_KEY)
    tasks = [
        (int(task_id), task_data['lesson_id'], task_data['task_name'], task_data['deadline'], task_data['completed'])
        for task_id, task_data in all_tasks.items()
        if task_data['lesson_id'] == lesson_id
    ]
    # Sort by completed status (False first), then by deadline
    tasks.sort(key=lambda x: (x[4], x[3]))
    return tasks

def get_all_lessons(page: ft.Page) -> list:
    lessons = page.client_storage.get(LESSONS_KEY)
    return [(int(lesson_id), lesson_data['lesson_name']) for lesson_id, lesson_data in lessons.items()]

def add_lesson(page: ft.Page, lesson_name: str):
    lessons = page.client_storage.get(LESSONS_KEY)
    new_id = _get_next_id(page, NEXT_LESSON_ID_KEY)
    lessons[str(new_id)] = {'lesson_name': lesson_name}
    page.client_storage.set(LESSONS_KEY, lessons)

def add_task(page: ft.Page, lesson_id: int, task_name: str, deadline: int):
    tasks = page.client_storage.get(TASKS_KEY)
    new_id = _get_next_id(page, NEXT_TASK_ID_KEY)
    tasks[str(new_id)] = {
        'lesson_id': lesson_id,
        'task_name': task_name,
        'deadline': deadline,
        'completed': False
    }
    page.client_storage.set(TASKS_KEY, tasks)

def update_task_completion(page: ft.Page, task_id: int, completed: bool):
    tasks = page.client_storage.get(TASKS_KEY)
    if str(task_id) in tasks:
        tasks[str(task_id)]['completed'] = completed
        page.client_storage.set(TASKS_KEY, tasks)

def update_task(page: ft.Page, task_id: int, task_name: str, deadline: int, completed: bool):
    tasks = page.client_storage.get(TASKS_KEY)
    if str(task_id) in tasks:
        tasks[str(task_id)] = {
            'lesson_id': tasks[str(task_id)]['lesson_id'], # Keep original lesson_id
            'task_name': task_name,
            'deadline': deadline,
            'completed': completed
        }
        page.client_storage.set(TASKS_KEY, tasks)

def delete_task(page: ft.Page, task_id: int):
    tasks = page.client_storage.get(TASKS_KEY)
    if str(task_id) in tasks:
        del tasks[str(task_id)]
        page.client_storage.set(TASKS_KEY, tasks)

def delete_lesson(page: ft.Page, lesson_id: int):
    lessons = page.client_storage.get(LESSONS_KEY)
    tasks = page.client_storage.get(TASKS_KEY)

    if str(lesson_id) in lessons:
        del lessons[str(lesson_id)]
        page.client_storage.set(LESSONS_KEY, lessons)

    # Delete associated tasks
    tasks_to_delete = [task_id for task_id, task_data in tasks.items() if task_data['lesson_id'] == lesson_id]
    for task_id in tasks_to_delete:
        del tasks[task_id]
    page.client_storage.set(TASKS_KEY, tasks)
