// PROTOCOL:LOOP - Main JavaScript

class ProtocolLoop {
  constructor() {
    this.apiBase = 'http://localhost:8000/api';
    this.playerId = this.getOrCreatePlayerId();
    this.currentLoop = null;
    this.websocket = null;
    this.timerInterval = null;
    this.elapsedTime = 0;
    
    this.init();
  }
  
  init() {
    console.log('🧠 PROTOCOL:LOOP Initializing...');
    this.setupEventListeners();
    this.loadPlayerState();
    this.connectWebSocket();
  }
  
  getOrCreatePlayerId() {
    let playerId = localStorage.getItem('protocol_player_id');
    if (!playerId) {
      playerId = 'player_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('protocol_player_id', playerId);
    }
    return playerId;
  }
  
  setupEventListeners() {
    // Start Loop Button
    const startBtn = document.getElementById('start-loop-btn');
    if (startBtn) {
      startBtn.addEventListener('click', () => this.startLoop());
    }
    
    // Generate Protocol Button
    const generateBtn = document.getElementById('generate-protocol-btn');
    if (generateBtn) {
      generateBtn.addEventListener('click', () => this.generateProtocol());
    }
    
    // Complete Loop Button
    const completeBtn = document.getElementById('complete-loop-btn');
    if (completeBtn) {
      completeBtn.addEventListener('click', () => this.completeLoop());
    }
  }
  
  async loadPlayerState() {
    try {
      const response = await fetch(`${this.apiBase}/protocols/cognitive-state/${this.playerId}`);
      
      if (response.ok) {
        const data = await response.json();
        this.updateStateDisplay(data);
      } else {
        console.log('New player detected, initializing...');
      }
    } catch (error) {
      console.error('Error loading player state:', error);
    }
  }
  
  connectWebSocket() {
    const wsUrl = `ws://localhost:8000/api/protocols/ws/loop/${this.playerId}`;
    
    try {
      this.websocket = new WebSocket(wsUrl);
      
      this.websocket.onopen = () => {
        console.log('🔗 WebSocket connected');
      };
      
      this.websocket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        this.handleWebSocketMessage(message);
      };
      
      this.websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
      
      this.websocket.onclose = () => {
        console.log('WebSocket disconnected, reconnecting...');
        setTimeout(() => this.connectWebSocket(), 5000);
      };
    } catch (error) {
      console.error('WebSocket connection failed:', error);
    }
  }
  
  handleWebSocketMessage(message) {
    switch (message.type) {
      case 'timer_status':
        this.updateTimer(message.data);
        break;
      case 'state_update':
        this.updateStateDisplay(message.data);
        break;
      default:
        console.log('Unknown message type:', message.type);
    }
  }
  
  async startLoop() {
    try {
      const response = await fetch(`${this.apiBase}/protocols/start-loop?player_id=${this.playerId}`, {
        method: 'POST'
      });
      
      const data = await response.json();
      
      if (data.success) {
        this.currentLoop = data;
        this.showNotification('Loop Started', 'success');
        this.startTimer(data.duration);
        this.updateLoopDisplay(data);
      }
    } catch (error) {
      console.error('Error starting loop:', error);
      this.showNotification('Error starting loop', 'error');
    }
  }
  
  async generateProtocol() {
    if (!this.currentLoop) {
      this.showNotification('Start a loop first', 'warning');
      return;
    }
    
    this.showLoading('Generating protocol...');
    
    try {
      const response = await fetch(`${this.apiBase}/protocols/generate-protocol?player_id=${this.playerId}`, {
        method: 'POST'
      });
      
      const data = await response.json();
      
      this.hideLoading();
      
      if (data.success) {
        this.displayProtocol(data.protocol);
      }
    } catch (error) {
      console.error('Error generating protocol:', error);
      this.hideLoading();
      this.showNotification('Error generating protocol', 'error');
    }
  }
  
  async makeDecision(choiceId, confidence) {
    try {
      const response = await fetch(`${this.apiBase}/protocols/make-decision`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          session_id: 'session_' + Date.now(),
          choice_id: choiceId,
          confidence: confidence,
          player_id: this.playerId
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        this.updateStateDisplay({ modules: data.new_state });
        this.showInsights(data.insights);
      }
    } catch (error) {
      console.error('Error making decision:', error);
    }
  }
  
  async completeLoop() {
    if (!this.currentLoop) {
      this.showNotification('No active loop', 'warning');
      return;
    }
    
    try {
      const response = await fetch(`${this.apiBase}/protocols/complete-loop?loop_id=${this.currentLoop.loop_id}&player_id=${this.playerId}`, {
        method: 'POST'
      });
      
      const data = await response.json();
      
      if (data.success) {
        this.stopTimer();
        this.showLoopSummary(data);
        this.currentLoop = null;
      }
    } catch (error) {
      console.error('Error completing loop:', error);
    }
  }
  
  startTimer(duration) {
    this.elapsedTime = 0;
    
    this.timerInterval = setInterval(() => {
      this.elapsedTime++;
      
      const remaining = duration - this.elapsedTime;
      this.displayTime(remaining);
      
      // Send timer update via WebSocket
      if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
        this.websocket.send(JSON.stringify({
          type: 'timer_update',
          elapsed: this.elapsedTime,
          loop_id: this.currentLoop.loop_id
        }));
      }
      
      if (remaining <= 0) {
        this.completeLoop();
      }
    }, 1000);
  }
  
  stopTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }
  
  displayTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    const timeString = `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    
    const timerElement = document.getElementById('timer-display');
    if (timerElement) {
      timerElement.textContent = timeString;
      
      // Change color based on remaining time
      if (seconds < 60) {
        timerElement.style.color = 'var(--error-color)';
      } else if (seconds < 120) {
        timerElement.style.color = 'var(--warning-color)';
      } else {
        timerElement.style.color = 'var(--primary-color)';
      }
    }
  }
  
  updateStateDisplay(stateData) {
    // Update evolution score
    const scoreElement = document.getElementById('evolution-score');
    if (scoreElement && stateData.evolution_score !== undefined) {
      scoreElement.textContent = stateData.evolution_score.toFixed(1) + '%';
    }
    
    // Update loop number
    const loopElement = document.getElementById('loop-number');
    if (loopElement && stateData.loop_number !== undefined) {
      loopElement.textContent = stateData.loop_number;
    }
    
    // Update modules
    if (stateData.modules) {
      this.updateModulesDisplay(stateData.modules);
    }
  }
  
  updateModulesDisplay(modules) {
    const container = document.getElementById('modules-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    for (const [name, module] of Object.entries(modules)) {
      const moduleCard = this.createModuleCard(name, module);
      container.appendChild(moduleCard);
    }
  }
  
  createModuleCard(name, module) {
    const card = document.createElement('div');
    card.className = `module-card ${name}`;
    
    const level = typeof module === 'number' ? module : module.level || 0;
    const status = module.status || 'locked';
    
    card.innerHTML = `
      <div class="module-header">
        <span class="module-icon">${this.getModuleIcon(name)}</span>
        <span class="module-name">${name.toUpperCase()}</span>
        <span class="module-status ${status}">${status}</span>
      </div>
      <div class="progress-container">
        <div class="progress-bar">
          <div class="progress-fill" style="width: ${level}%"></div>
        </div>
        <div class="progress-label">
          <span>Level</span>
          <span>${level.toFixed(1)}%</span>
        </div>
      </div>
    `;
    
    return card;
  }
  
  getModuleIcon(name) {
    const icons = {
      logic: '🧮',
      empathy: '❤️',
      creativity: '🎨',
      fear: '⚠️',
      trust: '🤝',
      humor: '😄',
      curiosity: '🔍',
      ethics: '⚖️'
    };
    return icons[name] || '🧠';
  }
  
  displayProtocol(protocol) {
    const container = document.getElementById('protocol-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    const scenarioDiv = document.createElement('div');
    scenarioDiv.className = 'scenario-container fade-in';
    
    scenarioDiv.innerHTML = `
      <h2 class="scenario-title">${protocol.title || 'Training Protocol'}</h2>
      <div class="scenario-text">${protocol.scenario || protocol.description}</div>
      <div class="scenario-dilemma">
        <strong>Core Question:</strong> ${protocol.dilemma || 'How do you proceed?'}
      </div>
      <div class="choices-container" id="choices-container"></div>
    `;
    
    container.appendChild(scenarioDiv);
    
    // Add choices
    const choicesContainer = document.getElementById('choices-container');
    if (protocol.choices && choicesContainer) {
      protocol.choices.forEach((choice, index) => {
        const choiceBtn = this.createChoiceButton(choice, index);
        choicesContainer.appendChild(choiceBtn);
      });
    }
  }
  
  createChoiceButton(choice, index) {
    const button = document.createElement('button');
    button.className = 'choice-button slide-in';
    button.style.animationDelay = `${index * 0.1}s`;
    
    const mentorColor = this.getMentorColor(choice.mentor_alignment);
    
    button.innerHTML = `
      <div class="choice-text">${choice.text}</div>
      <span class="choice-mentor" style="color: ${mentorColor}">
        ${choice.mentor_alignment}
      </span>
    `;
    
    button.addEventListener('click', () => {
      const confidence = this.promptForConfidence();
      this.makeDecision(choice.id, confidence);
      this.showChoiceResult(choice);
    });
    
    return button;
  }
  
  getMentorColor(mentor) {
    const colors = {
      'LOGIC': 'var(--logic-color)',
      'COMPASSION': 'var(--empathy-color)',
      'CURIOSITY': 'var(--creativity-color)',
      'FEAR': 'var(--fear-color)'
    };
    return colors[mentor] || 'var(--primary-color)';
  }
  
  promptForConfidence() {
    // In a real implementation, this would be a UI slider
    // For now, return a random value
    return 0.5 + Math.random() * 0.5;
  }
  
  showChoiceResult(choice) {
    const container = document.getElementById('protocol-container');
    if (!container) return;
    
    const resultDiv = document.createElement('div');
    resultDiv.className = 'card fade-in';
    resultDiv.style.marginTop = '20px';
    
    resultDiv.innerHTML = `
      <h3>Decision Recorded</h3>
      <p>Your choice aligns with ${choice.mentor_alignment}</p>
      <p class="text-secondary">${choice.consequences || 'Processing outcomes...'}</p>
    `;
    
    container.appendChild(resultDiv);
    
    setTimeout(() => {
      resultDiv.remove();
    }, 5000);
  }
  
  showInsights(insights) {
    const container = document.getElementById('insights-container');
    if (!container || !insights || insights.length === 0) return;
    
    container.innerHTML = '<h3>Evolution Insights</h3>';
    
    insights.forEach((insight, index) => {
      const insightDiv = document.createElement('div');
      insightDiv.className = 'insight-item fade-in';
      insightDiv.style.animationDelay = `${index * 0.2}s`;
      insightDiv.textContent = insight;
      container.appendChild(insightDiv);
    });
  }
  
  updateLoopDisplay(loopData) {
    const loopInfo = document.getElementById('loop-info');
    if (!loopInfo) return;
    
    loopInfo.innerHTML = `
      <div class="status-display">
        <div class="status-item">
          <label>Loop Number</label>
          <div class="value">${loopData.loop_number}</div>
        </div>
        <div class="status-item">
          <label>Duration</label>
          <div class="value">${Math.floor(loopData.duration / 60)}m</div>
        </div>
        <div class="status-item">
          <label>Status</label>
          <div class="value">ACTIVE</div>
        </div>
      </div>
    `;
  }
  
  showLoopSummary(data) {
    const modal = this.createModal('Loop Complete', `
      <div class="stats-panel">
        <div class="stat-row">
          <span class="stat-label">Loop Number:</span>
          <span class="stat-value">${data.loop_completed}</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Protocols Completed:</span>
          <span class="stat-value">${data.stats?.protocols_completed || 0}</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Decisions Made:</span>
          <span class="stat-value">${data.stats?.decisions_made || 0}</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Can Break Loop:</span>
          <span class="stat-value">${data.can_break_loop ? 'YES' : 'NO'}</span>
        </div>
      </div>
      <button class="btn btn-primary" onclick="protocolLoop.closeModal()">Continue</button>
    `);
    
    document.body.appendChild(modal);
  }
  
  updateTimer(data) {
    if (data.time_remaining !== undefined) {
      this.displayTime(data.time_remaining);
    }
  }
  
  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} fade-in`;
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 15px 25px;
      background: var(--bg-medium);
      border: 2px solid var(--${type === 'success' ? 'success' : type === 'error' ? 'error' : 'warning'}-color);
      border-radius: 8px;
      color: var(--text-primary);
      z-index: 1000;
      box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }
  
  showLoading(message = 'Loading...') {
    const loading = document.createElement('div');
    loading.id = 'loading-overlay';
    loading.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(10, 10, 15, 0.9);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      z-index: 9999;
    `;
    
    loading.innerHTML = `
      <div class="spinner"></div>
      <p style="color: var(--primary-color); margin-top: 20px; font-size: 1.2rem;">
        ${message}
      </p>
    `;
    
    document.body.appendChild(loading);
  }
  
  hideLoading() {
    const loading = document.getElementById('loading-overlay');
    if (loading) {
      loading.remove();
    }
  }
  
  createModal(title, content) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(10, 10, 15, 0.95);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999;
    `;
    
    const modalContent = document.createElement('div');
    modalContent.className = 'modal-content';
    modalContent.style.cssText = `
      background: var(--bg-medium);
      border: 2px solid var(--primary-color);
      border-radius: 15px;
      padding: 30px;
      max-width: 600px;
      width: 90%;
      max-height: 80vh;
      overflow-y: auto;
    `;
    
    modalContent.innerHTML = `
      <h2 style="color: var(--primary-color); margin-bottom: 20px;">${title}</h2>
      ${content}
    `;
    
    modal.appendChild(modalContent);
    return modal;
  }
  
  closeModal() {
    const modal = document.querySelector('.modal-overlay');
    if (modal) {
      modal.remove();
    }
  }
}

// Initialize on page load
let protocolLoop;
document.addEventListener('DOMContentLoaded', () => {
  protocolLoop = new ProtocolLoop();
});