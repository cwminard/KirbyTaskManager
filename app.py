from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = [{"task": "Play Mario Kart", "complete": False}]

@app.route('/', methods=['GET', 'POST'])
def index():
    global tasks

    if request.method == 'POST':
        for i in range(len(tasks)):
            tasks[i]['complete'] = f'task_{i}' in request.form
        return redirect('/')

    completed = sum(1 for task in tasks if task['complete'])
    total = len(tasks)

    if total == 0:
        photo = 'annoyed_kirby.png'
    elif completed == total:
        photo = 'happy_kirby.png'
    elif completed > 0:
        photo = 'sad_kirby.png'
    else:
        photo = 'annoyed_kirby.png'

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Kirby Task Manager</title>
        <style>
            body {{
                background-color: #ffc0cb;
                font-family: Verdana, sans-serif;
                color: white;
                margin: 0;
                padding: 20px;
            }}
            h1, h2 {{
                color: white;
            }}
            form {{
                margin-bottom: 20px;
            }}
            input[type="text"], select {{
                padding: 8px;
                border: none;
                border-radius: 6px;
                margin-right: 10px;
            }}
            button {{
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                background-color: white;
                color: #ff69b4;
                font-weight: bold;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #ffe6ef;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin-bottom: 10px;
            }}
            .image-container {{
                text-align: center;
                margin-top: 30px;
            }}
            img {{
                max-width: 500px;
                height: auto;
                border-radius: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                animation: fadeIn 1s ease-in-out;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
        </style>
    </head>
    <body>
        <h1>Kirby Task Manager</h1>

        <!-- Add New Task -->
        <form method="POST" action="/add">
            <input type="text" name="task" placeholder="New task..." required>
            <select name="status">
                <option value="incomplete">Incomplete</option>
                <option value="complete">Complete</option>
            </select>
            <button type="submit">Add Task</button>
        </form>

        <!-- Task Checklist -->
        <form method="POST" action="/">
            <ul>
    """

    for i, task in enumerate(tasks):
        checked = "checked" if task["complete"] else ""
        html += f"""
                <li>
                    <input type="checkbox" name="task_{i}" {checked}>
                    {task["task"]}
                </li>
        """

    html += """
            </ul>
            <button type="submit">Update Status</button>
        </form>

        <!-- Kirby Mood Image -->
        <div class="image-container">
            <h2>Your Progress</h2>
            <img src="/static/""" + photo + """">
        </div>
    </body>
    </html>
    """

    return html
    
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task_text = request.form.get('task')
        status = request.form.get('status')
        if task_text:
            tasks.append({"task": task_text, "complete": status == 'complete'})
        return redirect('/')
    
    return redirect('/')
    

if __name__ == '__main__':
    app.run(debug=True)