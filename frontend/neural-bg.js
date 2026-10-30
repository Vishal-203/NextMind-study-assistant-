
class NeuralBackground {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'neural-bg';
        this.ctx = this.canvas.getContext('2d');
        this.nodes = [];
        this.connections = [];
        this.numNodes = 60;
        this.maxDistance = 150;
        this.mouse = { x: null, y: null };

        this.init();
    }

    init() {
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.zIndex = '-1';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.opacity = '0.4';
        document.body.prepend(this.canvas);

        window.addEventListener('resize', () => this.resize());
        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });

        this.resize();
        this.createNodes();
        this.animate();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createNodes() {
        this.nodes = [];
        for (let i = 0; i < this.numNodes; i++) {
            this.nodes.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                pulse: Math.random() * Math.PI * 2,
                pulseSpeed: 0.02 + Math.random() * 0.03
            });
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Update and draw nodes
        this.nodes.forEach(node => {
            node.x += node.vx;
            node.y += node.vy;

            // Flowing wave movement
            node.y += Math.sin(Date.now() * 0.001 + node.x * 0.005) * 0.2;

            if (node.x < 0 || node.x > this.canvas.width) node.vx *= -1;
            if (node.y < 0 || node.y > this.canvas.height) node.vy *= -1;

            node.pulse += node.pulseSpeed;
            const glow = Math.sin(node.pulse) * 0.5 + 0.5;

            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, 1.5 + glow, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(0, 229, 255, ${0.2 + glow * 0.5})`;
            this.ctx.fill();
        });

        // Draw connections
        for (let i = 0; i < this.nodes.length; i++) {
            for (let j = i + 1; j < this.nodes.length; j++) {
                const dx = this.nodes[i].x - this.nodes[j].x;
                const dy = this.nodes[i].y - this.nodes[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < this.maxDistance) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.nodes[i].x, this.nodes[i].y);
                    this.ctx.lineTo(this.nodes[j].x, this.nodes[j].y);
                    const opacity = (1 - dist / this.maxDistance) * 0.2;
                    this.ctx.strokeStyle = `rgba(0, 229, 255, ${opacity})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.stroke();
                }
            }

            // Mouse interaction
            if (this.mouse.x !== null) {
                const dx = this.nodes[i].x - this.mouse.x;
                const dy = this.nodes[i].y - this.mouse.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 200) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.nodes[i].x, this.nodes[i].y);
                    this.ctx.lineTo(this.mouse.x, this.mouse.y);
                    const opacity = (1 - dist / 200) * 0.15;
                    this.ctx.strokeStyle = `rgba(0, 229, 255, ${opacity})`;
                    this.ctx.stroke();
                }
            }
        }

        requestAnimationFrame(() => this.animate());
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new NeuralBackground();
});
