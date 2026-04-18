import matplotlib.pyplot as plt

def generar_gantt(procesos):
    fig, ax = plt.subplots()

    for i, p in enumerate(procesos):
        ax.barh(p["archivo"], p["fin"] - p["inicio"], left=p["inicio"])

    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Procesos")
    ax.set_title("Diagrama de Gantt")

    plt.show()