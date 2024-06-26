document.addEventListener('DOMContentLoaded', () => {
    const servicesTableBody = document.querySelector('#services-table tbody');
    const addServiceForm = document.getElementById('add-service-form');

    async function fetchServices() {
        try {
            const response = await fetch('http://<YOUR_BACKEND_IP>:5000/services');
            if (!response.ok) throw new Error('Erro na rede');
            const services = await response.json();
            services.forEach(service => addServiceToTable(service));
        } catch (error) {
            console.error('Erro ao buscar serviços:', error);
        }
    }

    function addServiceToTable(service) {
        const row = servicesTableBody.insertRow();
        row.insertCell(0).textContent = service.id;
        row.insertCell(1).textContent = service.description;
        row.insertCell(2).textContent = service.status;
        row.insertCell(3).textContent = new Date(service.created_at).toLocaleString('pt-BR');
    }

    addServiceForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(addServiceForm);
        const data = {
            description: formData.get('description'),
            status: formData.get('status')
        };

        try {
            const response = await fetch('http://<YOUR_BACKEND_IP>:5000/services', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Erro na rede');
            const newService = await response.json();
            addServiceToTable(newService);
            addServiceForm.reset();
        } catch (error) {
            console.error('Erro ao adicionar serviço:', error);
        }
    });

    fetchServices();
});
