import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import numpy as np

class PhaseVisualizer:
    def __init__(self, log_returns, velocity, acceleration):
        self.log_returns = log_returns
        self.velocity = velocity
        self.acceleration = acceleration
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.n = len(log_returns)
        self.angle = 0
        self.traj = None
        self.scatter = None
        self.setup_plot()

    def setup_plot(self):
        self.ax.set_xlabel('Log Return', fontsize=14)
        self.ax.set_ylabel('Velocity', fontsize=14)
        self.ax.set_zlabel('Acceleration', fontsize=14)
        self.ax.set_title('BTC Market Phase Space Trajectory', fontsize=16, fontweight='bold')
        self.ax.grid(True)

    def update(self, frame):
        x = self.log_returns[:frame]
        y = self.velocity[:frame]
        z = self.acceleration[:frame]
        # Color mapping
        colors = plt.cm.viridis(np.linspace(0, 1, len(x)))
        self.ax.cla()
        self.setup_plot()
        # Draw trajectory
        if len(x) > 1:
            for i in range(len(x)-1):
                self.ax.plot([x[i], x[i+1]], [y[i], y[i+1]], [z[i], z[i+1]], color=colors[i], linewidth=3)
        # Draw scatter points
        self.ax.scatter(x, y, z, c=colors, s=30, alpha=0.8)
        # Camera rotation
        self.angle += 0.5
        self.ax.view_init(elev=30, azim=self.angle)
        return []

    def animate(self):
        anim = FuncAnimation(self.fig, self.update, frames=self.n, interval=20, blit=False)
        plt.tight_layout()
        plt.show()
