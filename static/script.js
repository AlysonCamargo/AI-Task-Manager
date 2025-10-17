// ==================== CONFIGURAÇÃO DA API ====================
const API_URL = 'http://localhost:5000/api';

// ==================== ESTADO DA APLICAÇÃO ====================
let currentFilter = {
    status: '',
    priority: ''
};

let editingTaskId = null;

// ==================== ELEMENTOS DO DOM ====================
const elements = {
    // Stats
    totalTasks: document.getElementById('totalTasks'),
    pendingTasks: document.getElementById('pendingTasks'),
    inProgressTasks: document.getElementById('inProgressTasks'),
    completedTasks: document.getElementById('completedTasks'),
    
    // Containers
    tasksContainer: document.getElementById('tasksContainer'),
    suggestionsContainer: document.getElementById('suggestionsContainer'),
    taskCount: document.getElementById('taskCount'),
    
    // Filters
    statusFilter: document.getElementById('statusFilter'),
    priorityFilter: document.getElementById('priorityFilter'),
    smartSortBtn: document.getElementById('smartSortBtn'),
    
    // Modal
    taskModal: document.getElementById('taskModal'),
    taskForm: document.getElementById('taskForm'),
    newTaskBtn: document.getElementById('newTaskBtn'),
    closeModal: document.getElementById('closeModal'),
    cancelBtn: document.getElementById('cancelBtn'),
    modalTitle: document.getElementById('modalTitle'),
    
    // Form Fields
    taskId: document.getElementById('taskId'),
    taskTitle: document.getElementById('taskTitle'),
    taskDescription: document.getElementById('taskDescription'),
    taskPriority: document.getElementById('taskPriority'),
    taskCategory: document.getElementById('taskCategory'),
    taskDueDate: document.getElementById('taskDueDate'),
    taskEstimatedTime: document.getElementById('taskEstimatedTime')
};

// ==================== INICIALIZAÇÃO ====================
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    loadStats();
    loadTasks();
    loadAISuggestions();
}

function setupEventListeners() {
    // Modal
    elements.newTaskBtn.addEventListener('click', openNewTaskModal);
    elements.closeModal.addEventListener('click', closeModal);
    elements.cancelBtn.addEventListener('click', closeModal);
    elements.taskForm.addEventListener('submit', handleTaskSubmit);
    
    // Filters
    elements.statusFilter.addEventListener('change', handleFilterChange);
    elements.priorityFilter.addEventListener('change', handleFilterChange);
    elements.smartSortBtn.addEventListener('click', handleSmartSort);
    
    // Close modal on outside click
    elements.taskModal.addEventListener('click', (e) => {
        if (e.target === elements.taskModal) {
            closeModal();
        }
    });
}

// ==================== API CALLS ====================
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${API_URL}${endpoint}`, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Request failed');
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        alert(`Erro: ${error.message}`);
        throw error;
    }
}

// ==================== CARREGAR DADOS ====================
async function loadStats() {
    try {
        const data = await apiCall('/stats/overview');
        const stats = data.stats;
        
        elements.totalTasks.textContent = stats.total_tasks;
        elements.pendingTasks.textContent = stats.pending;
        elements.inProgressTasks.textContent = stats.in_progress;
        elements.completedTasks.textContent = stats.completed;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadTasks() {
    try {
        const params = new URLSearchParams(currentFilter);
        const data = await apiCall(`/tasks?${params}`);
        
        renderTasks(data.tasks);
        elements.taskCount.textContent = `${data.count} tarefa(s)`;
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

async function loadAISuggestions() {
    try {
        const data = await apiCall('/ai/suggestions');
        renderSuggestions(data.suggestions);
    } catch (error) {
        console.error('Error loading suggestions:', error);
    }
}

// ==================== RENDERIZAÇÃO ====================
function renderTasks(tasks) {
    elements.tasksContainer.innerHTML = '';
    
    if (tasks.length === 0) {
        elements.tasksContainer.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #6b7280;">
                <p style="font-size: 1.5em; margin-bottom: 10px;">📭</p>
                <p>Nenhuma tarefa encontrada. Crie uma nova!</p>
            </div>
        `;
        return;
    }
    
    tasks.forEach(task => {
        const taskCard = createTaskCard(task);
        elements.tasksContainer.appendChild(taskCard);
    });
}

function createTaskCard(task) {
    const card = document.createElement('div');
    card.className = `task-card ${task.status === 'completed' ? 'completed' : ''}`;
    
    const priorityEmojis = {
        urgent: '🔴',
        high: '🟠',
        medium: '🟡',
        low: '🟢'
    };
    
    const statusLabels = {
        pending: 'Pendente',
        in_progress: 'Em Progresso',
        completed: 'Concluída'
    };
    
    card.innerHTML = `
        <div class="task-header">
            <div>
                <div class="task-title">${task.title}</div>
                ${task.description ? `<div class="task-description">${task.description}</div>` : ''}
            </div>
        </div>
        
        <div class="task-meta">
            <span class="task-badge badge-priority ${task.priority}">
                ${priorityEmojis[task.priority]} ${task.priority.toUpperCase()}
            </span>
            ${task.category ? `<span class="task-badge badge-category">📂 ${task.category}</span>` : ''}
            ${task.estimated_time ? `<span class="task-badge badge-time">⏱️ ${task.estimated_time}min</span>` : ''}
            ${task.due_date ? `<span class="task-badge" style="background: #8b5cf6; color: white;">📅 ${formatDate(task.due_date)}</span>` : ''}
        </div>
        
        <div class="task-actions">
            ${task.status !== 'completed' ? `
                <button class="task-btn complete" onclick="completeTask(${task.id})">
                    ✅ Concluir
                </button>
            ` : ''}
            <button class="task-btn edit" onclick="editTask(${task.id})">
                ✏️ Editar
            </button>
            <button class="task-btn delete" onclick="deleteTask(${task.id})">
                🗑️ Excluir
            </button>
        </div>
    `;
    
    return card;
}

function renderSuggestions(suggestions) {
    elements.suggestionsContainer.innerHTML = '';
    
    suggestions.forEach(suggestion => {
        const card = document.createElement('div');
        card.className = `suggestion-card ${suggestion.type}`;
        
        card.innerHTML = `
            <div class="suggestion-header">
                <span class="suggestion-icon">${suggestion.icon}</span>
                <span class="suggestion-title">${suggestion.title}</span>
            </div>
            <p class="suggestion-message">${suggestion.message}</p>
        `;
        
        elements.suggestionsContainer.appendChild(card);
    });
}

// ==================== MODAL ====================
function openNewTaskModal() {
    editingTaskId = null;
    elements.modalTitle.textContent = 'Nova Tarefa';
    elements.taskForm.reset();
    elements.taskModal.classList.add('active');
}

function openEditTaskModal(task) {
    editingTaskId = task.id;
    elements.modalTitle.textContent = 'Editar Tarefa';
    
    elements.taskTitle.value = task.title;
    elements.taskDescription.value = task.description || '';
    elements.taskPriority.value = task.priority;
    elements.taskCategory.value = task.category || '';
    elements.taskEstimatedTime.value = task.estimated_time || '';
    
    if (task.due_date) {
        const date = new Date(task.due_date);
        elements.taskDueDate.value = date.toISOString().slice(0, 16);
    }
    
    elements.taskModal.classList.add('active');
}

function closeModal() {
    elements.taskModal.classList.remove('active');
    elements.taskForm.reset();
    editingTaskId = null;
}

// ==================== CRUD OPERATIONS ====================
async function handleTaskSubmit(e) {
    e.preventDefault();
    
    const taskData = {
        title: elements.taskTitle.value,
        description: elements.taskDescription.value || null,
        priority: elements.taskPriority.value,
        category: elements.taskCategory.value || null,
        due_date: elements.taskDueDate.value || null,
        estimated_time: elements.taskEstimatedTime.value ? parseInt(elements.taskEstimatedTime.value) : null
    };
    
    try {
        if (editingTaskId) {
            await apiCall(`/tasks/${editingTaskId}`, 'PUT', taskData);
        } else {
            await apiCall('/tasks', 'POST', taskData);
        }
        
        closeModal();
        loadTasks();
        loadStats();
        loadAISuggestions();
    } catch (error) {
        console.error('Error saving task:', error);
    }
}

async function editTask(taskId) {
    try {
        const data = await apiCall(`/tasks/${taskId}`);
        openEditTaskModal(data.task);
    } catch (error) {
        console.error('Error loading task:', error);
    }
}

async function completeTask(taskId) {
    try {
        await apiCall(`/tasks/${taskId}`, 'PUT', { status: 'completed' });
        loadTasks();
        loadStats();
        loadAISuggestions();
    } catch (error) {
        console.error('Error completing task:', error);
    }
}

async function deleteTask(taskId) {
    if (!confirm('Tem certeza que deseja excluir esta tarefa?')) {
        return;
    }
    
    try {
        await apiCall(`/tasks/${taskId}`, 'DELETE');
        loadTasks();
        loadStats();
        loadAISuggestions();
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}

// ==================== FILTERS & SORTING ====================
function handleFilterChange() {
    currentFilter.status = elements.statusFilter.value;
    currentFilter.priority = elements.priorityFilter.value;
    loadTasks();
}

async function handleSmartSort() {
    try {
        const data = await apiCall('/ai/smart-sort', 'POST');
        renderTasks(data.sorted_tasks);
        elements.taskCount.textContent = `${data.sorted_tasks.length} tarefa(s) (ordenadas por IA)`;
    } catch (error) {
        console.error('Error smart sorting:', error);
    }
}

// ==================== UTILIDADES ====================
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = date - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) {
        return `Atrasada ${Math.abs(diffDays)}d`;
    } else if (diffDays === 0) {
        return 'Hoje';
    } else if (diffDays === 1) {
        return 'Amanhã';
    } else {
        return `${diffDays} dias`;
    }
}
