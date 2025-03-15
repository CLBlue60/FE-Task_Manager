document.addEventListener('DOMContentLoaded', () => {
  fetchTasks();

  document.addEventListener('click', function (event) {
    if (event.target.classList.contains('delete-task-btn')) {
      event.preventDefault();
      const taskId = event.target.getAttribute('data-task-id');
      deleteTask(taskId);
    }
  });
});

function fetchTasks() {
  fetch('/api/tasks')
    .then(response => response.json())
    .then(data => {
      const taskList = document.getElementById('task-list');
      taskList.innerHTML = '';
      data.tasks.forEach(task => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <th scope="row">${task.id}</th>
          <td>${task.name}</td>
          <td>${task.summary}</td>
          <td>${task.description}</td>
          <td>
            <a href="/tasks/${task.id}" class="btn btn-warning">
              <i class="bi bi-eye"></i>
            </a>
            <a href="/tasks/${task.id}/delete" class="btn btn-danger delete-task-btn" data-task-id="${task.id}">
              <i class="bi bi-trash"></i>
            </a>
          </td>
        `;
        taskList.appendChild(row);
      });
    });
}

function deleteTask(taskId) {
  fetch(`/tasks/${taskId}/delete`, { method: 'POST' })
    .then(response => {
      if (response.ok) {
        fetchTasks();
      } else {
        alert('Failed to delete task');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while deleting the task');
    });
}
