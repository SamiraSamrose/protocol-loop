// PROTOCOL:LOOP - Visualization Components

class Visualizations {
  constructor() {
    this.charts = {};
    this.colors = {
      logic: '#00ffff',
      empathy: '#ff69b4',
      creativity: '#ffd700',
      fear: '#8b00ff',
      trust: '#00ff00',
      humor: '#ff6347',
      curiosity: '#ffa500',
      ethics: '#4169e1'
    };
  }
  
  // Evolution Score Chart
  createEvolutionChart(containerId, data) {
    const canvas = document.getElementById(containerId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Draw grid
    this.drawGrid(ctx, width, height);
    
    // Draw evolution line
    this.drawEvolutionLine(ctx, data, width, height);
    
    // Draw data points
    this.drawDataPoints(ctx, data, width, height);
  }
  
  drawGrid(ctx, width, height) {
    ctx.strokeStyle = 'rgba(0, 255, 255, 0.1)';
    ctx.lineWidth = 1;
    
    // Vertical lines
    for (let x = 0; x < width; x += 50) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    
    // Horizontal lines
    for (let y = 0; y < height; y += 50) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }
  }
  
  drawEvolutionLine(ctx, data, width, height) {
    if (!data || data.length < 2) return;
    
    ctx.strokeStyle = '#00ffff';
    ctx.lineWidth = 3;
    ctx.shadowBlur = 10;
    ctx.shadowColor = '#00ffff';
    
    ctx.beginPath();
    
    data.forEach((point, index) => {
      const x = (index / (data.length - 1)) * width;
      const y = height - (point.score / 100) * height;
      
      if (index === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });
    
    ctx.stroke();
    ctx.shadowBlur = 0;
  }
  
  drawDataPoints(ctx, data, width, height) {
    data.forEach((point, index) => {
      const x = (index / (data.length - 1)) * width;
      const y = height - (point.score / 100) * height;
      
      ctx.fillStyle = '#ff00ff';
      ctx.shadowBlur = 15;
      ctx.shadowColor = '#ff00ff';
      
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fill();
    });
    
    ctx.shadowBlur = 0;
  }
  
  // Cognitive Modules Radar Chart
  createRadarChart(containerId, modules) {
    const canvas = document.getElementById(containerId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) / 2 - 40;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    const moduleNames = Object.keys(modules);
    const angleStep = (Math.PI * 2) / moduleNames.length;
    
    // Draw background circles
    this.drawRadarGrid(ctx, centerX, centerY, radius, moduleNames.length);
    
    // Draw labels
    this.drawRadarLabels(ctx, centerX, centerY, radius, moduleNames, angleStep);
    
    // Draw data
    this.drawRadarData(ctx, centerX, centerY, radius, modules, angleStep);
  }
  
  drawRadarGrid(ctx, centerX, centerY, radius, segments) {
    ctx.strokeStyle = 'rgba(0, 255, 255, 0.2)';
    ctx.lineWidth = 1;
    
    // Concentric circles
    for (let i = 1; i <= 5; i++) {
      const r = (radius / 5) * i;
      ctx.beginPath();
      ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
      ctx.stroke();
    }
    
    // Radial lines
    const angleStep = (Math.PI * 2) / segments;
    for (let i = 0; i < segments; i++) {
      const angle = angleStep * i - Math.PI / 2;
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(
        centerX + Math.cos(angle) * radius,
        centerY + Math.sin(angle) * radius
      );
      ctx.stroke();
    }
  }
  
  drawRadarLabels(ctx, centerX, centerY, radius, labels, angleStep) {
    ctx.fillStyle = '#00ffff';
    ctx.font = '14px "Courier New"';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    labels.forEach((label, i) => {
      const angle = angleStep * i - Math.PI / 2;
      const x = centerX + Math.cos(angle) * (radius + 25);
      const y = centerY + Math.sin(angle) * (radius + 25);
      
      ctx.fillText(label.toUpperCase(), x, y);
    });
  }
  
  drawRadarData(ctx, centerX, centerY, radius, modules, angleStep) {
    const moduleNames = Object.keys(modules);
    
    // Fill
    ctx.fillStyle = 'rgba(0, 255, 255, 0.2)';
    ctx.beginPath();
    
    moduleNames.forEach((name, i) => {
      const value = typeof modules[name] === 'number' ? modules[name] : modules[name].level || 0;
      const angle = angleStep * i - Math.PI / 2;
      const r = (value / 100) * radius;
      const x = centerX + Math.cos(angle) * r;
      const y = centerY + Math.sin(angle) * r;
      
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });
    
    ctx.closePath();
    ctx.fill();
    
    // Stroke
    ctx.strokeStyle = '#00ffff';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Points
    moduleNames.forEach((name, i) => {
      const value = typeof modules[name] === 'number' ? modules[name] : modules[name].level || 0;
      const angle = angleStep * i - Math.PI / 2;
      const r = (value / 100) * radius;
      const x = centerX + Math.cos(angle) * r;
      const y = centerY + Math.sin(angle) * r;
      
      ctx.fillStyle = this.colors[name] || '#ffffff';
      ctx.shadowBlur = 10;
      ctx.shadowColor = ctx.fillStyle;
      
      ctx.beginPath();
      ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fill();
    });
    
    ctx.shadowBlur = 0;
  }
  
  // Progress Bar Animation
  animateProgressBar(elementId, targetValue, duration = 1000) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const startValue = parseFloat(element.style.width) || 0;
    const startTime = performance.now();
    
    const animate = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      const currentValue = startValue + (targetValue - startValue) * this.easeOutCubic(progress);
      element.style.width = currentValue + '%';
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    
    requestAnimationFrame(animate);
  }
  
  easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }
  
  // Particle System for Background
  createParticleSystem(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const particles = [];
    const particleCount = 100;
    
    class Particle {
      constructor(width, height) {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.radius = Math.random() * 2 + 1;
        this.opacity = Math.random() * 0.5 + 0.3;
      }
      
      update(width, height) {
        this.x += this.vx;
        this.y += this.vy;
        
        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;
      }
      
      draw(ctx) {
        ctx.fillStyle = `rgba(0, 255, 255, ${this.opacity})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
      }
    }
    
    // Initialize particles
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle(canvas.width, canvas.height));
    }
    
    // Animation loop
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      particles.forEach(particle => {
        particle.update(canvas.width, canvas.height);
        particle.draw(ctx);
      });
      
      // Draw connections
      this.drawConnections(ctx, particles);
      
      requestAnimationFrame(animate);
    };
    
    animate();
  }
  
  drawConnections(ctx, particles) {
    ctx.strokeStyle = 'rgba(0, 255, 255, 0.1)';
    ctx.lineWidth = 0.5;
    
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 100) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
  }
  
  // Heat Map for Decision Patterns
  createDecisionHeatmap(containerId, decisionData) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const mentors = ['LOGIC', 'COMPASSION', 'CURIOSITY', 'FEAR'];
    const confidenceLevels = ['Low', 'Medium', 'High'];
    
    let html = '<div class="heatmap">';
    html += '<div class="heatmap-row header"><div class="heatmap-cell"></div>';
    
    mentors.forEach(mentor => {
      html += `<div class="heatmap-cell">${mentor}</div>`;
    });
    html += '</div>';
    
    confidenceLevels.forEach(level => {
      html += `<div class="heatmap-row"><div class="heatmap-cell label">${level}</div>`;
      
      mentors.forEach(mentor => {
        const value = decisionData[mentor]?.[level] || 0;
        const intensity = Math.min(value / 10, 1);
        const color = `rgba(0, 255, 255, ${intensity})`;
        
        html += `<div class="heatmap-cell" style="background: ${color}">${value}</div>`;
      });
      
      html += '</div>';
    });
    
    html += '</div>';
    container.innerHTML = html;
  }
}

// Initialize visualizations
const visualizations = new Visualizations();