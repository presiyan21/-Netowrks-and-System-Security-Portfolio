import random
import time

def simulate_worm(network_size=200, attempts_per_host=3, infection_chance=0.5, steps=20):
    """
    Simulate a worm spreading through a virtual network.
    """

    # 0 = clean, 1 = infected
    network = [0] * network_size
    network[0] = 1   # Starting infection point

    infection_history = []

    for step in range(steps):
        new_infections = []
        
        for host_id, status in enumerate(network):
            if status == 1:
                # Infected host tries to spread
                for _ in range(attempts_per_host):
                    target = random.randint(0, network_size - 1)

                    if network[target] == 0 and random.random() < infection_chance:
                        new_infections.append(target)

        # Update infections
        for target in new_infections:
            network[target] = 1

        infected_count = sum(network)
        infection_history.append(infected_count)

        print(f"Step {step+1}: {infected_count}/{network_size} hosts infected")

        time.sleep(0.2)

    return infection_history


if __name__ == "__main__":
    simulate_worm(
        network_size=200,
        attempts_per_host=5,
        infection_chance=0.4,
        steps=25
    )
