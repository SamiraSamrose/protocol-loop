// PROTOCOL:LOOP - Neural Network Visualization using D3.js-like approach

class NeuralMap {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    
    this.ctx = this.canvas.getContext('2d');
    this.width = this.canvas.width;
    this.height = this.canvas.height;
    this.nodes = [];
    this.links = [];
    this.animationFrame = null;
    
    this.init();
  }
  
  init() {
    this.setupInteraction();
    this.animate();
  }
  
  setupInteraction() {
    let isDragging = false;
    let selectedNode = null;
    
    this.canvas.addEventListener('mousedown', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      selectedNode = this.findNodeAt(x, y);
      if (selectedNode) {
        isDragging = true;
      }
    });
    
    this.canvas.addEventListener('mousemove', (e) => {
      if (isDragging && selectedNode) {
        const rect = this.canvas.getBoundingClientRect();
        selectedNode.x = e.clientX - rect.left;
        selectedNode.y = e.clientY - rect.top;
      }
    });
    
    this.canvas.addEventListener('mouseup', () => {
      isDragging = false;
      selectedNode = null;
    });
  }
  
  findNodeAt(x, y) {
    return this.nodes.find(node => {
      const dx = node.x - x;
      const dy = node.y - y;
      return Math.sqrt(dx * dx + dy * dy) < node.radius;
    });
  }
  
  loadData(treeData) {
    this.nodes = [];
    this.links = [];
    
    // Convert tree data to nodes
    if (treeData.nodes) {
      treeData.nodes.forEach((nodeData, index) => {
        this.nodes.push({
          id: nodeData.id,
          x: Math.random() * this.width,
          y: Math.random() * this.height,
          vx: 0,
          vy: 0,
          radius: 15 + (nodeData.level / 100) * 20,
          level: nodeData.level,
          status: nodeData.status,
          color: nodeData.color,
          icon: nodeData.icon
        });
      });
    }
    
    // Convert tree data to links
    if (treeData.links) {
      treeData.links.forEach(linkData => {
        const source = this.nodes.find(n => n.id === linkData.source);
        const target = this.nodes.find(n => n.id === linkData.target);
        
        if (source && target) {
          this.links.push({
            source,
            target,
            strength: linkData.strength || 0.5
          });
        }
      });
    }
    
    // Initialize physics simulation
    this.initPhysics();
  }
  
  initPhysics() {
    // Apply force-directed layout
    const centerX = this.width / 2;
    const centerY = this.height / 2;
    
    // Position nodes in a circle initially
    this.nodes.forEach((node, index) => {
      const angle = (index / this.nodes.length) * Math.PI * 2;
      const radius = Math.min(this.width, this.height) / 3;
      node.x = centerX + Math.cos(angle) * radius;
      node.y = centerY + Math.sin(angle) * radius;
    });
  }
  
  update() {
    const centerX = this.width / 2;
    const centerY = this.height / 2;
    
    // Apply forces
    this.nodes.forEach(node => {
      // Center attraction
      const dx = centerX - node.x;
      const dy = centerY - node.y;
      node.vx += dx * 0.001;
      node.vy += dy * 0.001;
      
      // Node repulsion
      this.nodes.forEach(other => {
        if (node !== other) {
          const dx = node.x - other.x;
          const dy = node.y - other.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          
          if (dist < 100 && dist > 0) {
            const force = 100 / (dist * dist);
            node.vx += (dx / dist) * force;
            node.vy += (dy / dist) * force;
          }
        }
      });
    });
    
    // Link attraction
    this.links.forEach(link => {
      const dx = link.target.x - link.source.x;
      const dy = link.target.y - link.source.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      
      if (dist > 0) {
        const force = (dist - 150) * 0.01 * link.strength;
        const fx = (dx / dist) * force;
        const fy = (dy / dist) * force;
        
        link.source.vx += fx;
        link.source.vy += fy;
        link.target.vx -= fx;
        link.target.vy -= fy;
      }
    });
    
    // Update positions with damping
    this.nodes.forEach(node => {
      node.x += node.vx;
      node.y += node.vy;
      node.vx *= 0.9;
      node.vy *= 0.9;
      
      // Keep nodes in bounds
      node.x = Math.max(node.radius, Math.min(this.width - node.radius, node.x));
      node.y = Math.max(node.radius, Math.min(this.height - node.radius, node.y));
    });
  }
  
  draw() {
    // Clear canvas
    this.ctx.clearRect(0, 0, this.width, this.height);
    
    // Draw links
    this.links.forEach(link => {
      this.ctx.strokeStyle = `rgba(0, 255, 255, ${link.strength * 0.5})`;
      this.ctx.lineWidth = link.strength * 3;
      this.ctx.shadowBlur = 10;
      this.ctx.shadowColor = 'rgba(0, 255, 255, 0.5)';
      
      this.ctx.beginPath();
      this.ctx.moveTo(link.source.x, link.source.y);
      this.ctx.lineTo(link.target.x, link.target.y);
      this.ctx.stroke();
    });
    
    this.ctx.shadowBlur = 0;
    
    // Draw nodes
    this.nodes.forEach(node => {
      // Glow effect
      const gradient = this.ctx.createRadialGradient(
        node.x, node.y, 0,
        node.x, node.y, node.radius
      );
      gradient.addColorStop(0, node.color);
      gradient.addColorStop(1, 'transparent');
      
      this.ctx.fillStyle = gradient;
      this.ctx.shadowBlur = 20;
      this.ctx.shadowColor = node.color;
      
      this.ctx.beginPath();
      this.ctx.arc(node.x, node.y, node.radius * 1.5, 0, Math.PI * 2);
      this.ctx.fill();
      
      // Node circle
      this.ctx.fillStyle = node.color;
      this.ctx.shadowBlur = 15;
      
      this.ctx.beginPath();
      this.ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
      this.ctx.fill();
      
      // Status indicator
      const statusColor = this.getStatusColor(node.status);
      this.ctx.fillStyle = statusColor;
      this.ctx.shadowBlur = 5;
      
      this.ctx.beginPath();
      this.ctx.arc(node.x, node.y, node.radius * 0.4, 0, Math.PI * 2);
      this.ctx.fill();
      
      this.ctx.shadowBlur = 0;
      
      // Label
      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = '12px "Courier New"';
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(node.id.toUpperCase(), node.x, node.y + node.radius + 15);
      
      // Icon
      this.ctx.font = '20px "Courier New"';
      this.ctx.fillText(node.icon, node.x, node.y);
    });
  }
  
  getStatusColor(status) {
    const colors = {
      'locked': '#444444',
      'nascent': '#ffff00',
      'developing': '#00ffff',
      'active': '#00ff00',
      'mastered': '#ff00ff'
    };
    return colors[status] || '#ffffff';
  }
  
  animate() {
    this.update();
    this.draw();
    this.animationFrame = requestAnimationFrame(() => this.animate());
  }
  
  stop() {
    if (this.animationFrame) {
      cancelAnimationFrame(this.animationFrame);
    }
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = NeuralMap;
}