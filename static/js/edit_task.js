document.getElementById('edit-task-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());
    const taskId = document.getElementById('edit-task-form').dataset.taskId;

    console.log('Form data:', data); // Debugging log

    fetch(`/tasks/${taskId}/edit`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log('Response status:', response.status); // Debugging log
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data); // Debugging log
        if (data.ok) {
            window.location.href = '/tasks';
        } else {
            alert(data.error || 'Failed to update task');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the task');
    });
});
