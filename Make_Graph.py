import matplotlib.pyplot as plt
import datetime
import Paddle

# Creates a file to be used to display a graph of the evolutions
def create_file():
    time = datetime.datetime.now()
    filename = "pongML_"+time.strftime("%j")+"_"+time.strftime("%H")+"-"+time.strftime("%M")+"-"+time.strftime("%S")+".txt" # %j for day between 1 and 365, %f for time in milliseconds
    f = open(filename, "w+")
    f.close()
    return filename

# Adds the winning coefficients and the scores to the file
def add_to_file(filename, winner, score, winners_count):
    if winner != None:
        new_line = str(winner.coefficients)+","+str(score)+","+str(winners_count)+"\n"
    else:
        new_line = str(winner)+","+str(score)+","+str(winners_count)+"\n"
    with open(filename, "a") as f:
        f.write(new_line)

# Extracts data from the text file
def read_file(filename):
    with open(filename, "r") as f:
        entire_file = f.read()
        lines = entire_file.split("\n")
        generations = []
        for line in lines:
            try:
                line = line.replace("[", "")
                line = line.replace("]", "")
                line = line.replace(" ", "")
                tmp = line.split(",")

                for i in range(len(tmp)):
                    if "." in tmp[i]:
                        tmp[i] = float(tmp[i])
                    else:
                        tmp[i] = int(tmp[i])
                        
                coefficients = tmp[0:3]
                generations.append([coefficients, tmp[3], tmp[4]])
            except Exception as e:
                pass
        
        return generations

# Uses the data from the file, draw a set of graphs
def draw_graphs(filename):
    generations = read_file(filename)
    coefficients = []
    scores = []
    winners_count = []
    gen_count = []

    count = 0
    for gen in generations:
        count += 1
        coefficients.append(gen[0])
        scores.append(gen[1])
        winners_count.append(gen[2])
        gen_count.append(count)

    paddles_x_coeff = []
    balls_x_coeff = []
    balls_y_coeff = []
    for coeff in coefficients:
        paddles_x_coeff.append(coeff[0])
        balls_x_coeff.append(coeff[1])
        balls_y_coeff.append(coeff[2])

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 4))
    fig.suptitle("Graphs",
                fontsize=14, fontweight='bold')
    ax = axes.ravel()

    ax[0].plot(gen_count, paddles_x_coeff)
    ax[0].set_title("Coefficient for paddle x vs time")
    ax[0].set(xlabel="Generation", ylabel="Paddle x coefficient")

    ax[1].plot(gen_count, balls_x_coeff)
    ax[1].set_title("Coefficient for ball x vs time")
    ax[1].set(xlabel="Generation", ylabel="Ball x coefficient")

    ax[2].plot(gen_count, balls_y_coeff)
    ax[2].set_title("Coefficient for ball y vs time")
    ax[2].set(xlabel="Generation", ylabel="Ball y coefficient")

    ax[3].plot(gen_count, scores)
    ax[3].set_title("Maximum scores vs time")
    ax[3].set(xlabel="Generation", ylabel="Score")

    ax[4].plot(gen_count, winners_count)
    ax[4].set_title("Number of winners per generation")
    ax[4].set(xlabel="Generation", ylabel="Number of winners")

    ax[5].axis('off')

    # Source: https://stackoverflow.com/questions/7917107/add-footnote-under-the-x-axis-using-matplotlib
    plt.figtext(0.8, 0.95,
                "Optimal Coefficients = "+str(coefficients[-1:][0]),
                ha="center",
                bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    fig.tight_layout()

    # Saves the graph as an image
    img_filename = filename[:-3] + "png"
    plt.savefig(img_filename, transparent=False)

    plt.show()