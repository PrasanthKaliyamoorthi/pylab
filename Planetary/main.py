import rebound

def main():
    sim = rebound.Simulation()
    sim.add(m=1.0)
    sim.add(m=1.0e-3, a=1.0)
    sim.integrate(1000.)
    sim.status()

if __name__ == "__main__":
    main()
