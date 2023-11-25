import matplotlib.pyplot as plt
import numpy as np

# Define a linear function: f(x) = 2x + 3
def linear_function(x):
    return 2 * x + 3

# Generate x values
x = np.linspace(-5, 5, 100)

# Calculate corresponding y values using the linear function
y = linear_function(x)

# Plot the linear function
plt.figure(figsize=(8, 6))
plt.plot(x, y, label='f(x) = 2x + 3', color='blue')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Graph of the Linear Function')
plt.legend()
plt.grid(True)
plt.show()
