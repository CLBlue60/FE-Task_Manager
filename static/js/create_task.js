document.getElementById('create-task-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    console.log('Form data:', data);

    fetch('/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.ok) {
            window.location.href = '/tasks';
        } else {
            alert(data.error || 'Failed to create task');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while creating the task');
    });
});
