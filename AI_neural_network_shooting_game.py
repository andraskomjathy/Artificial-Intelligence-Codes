#Hello and welcome! This is a very simple shooting game
#driven by a single-layer neural network
#with really minimalist graphics. The AI plays the
#green square and the enemy plays the red squares.
#AI has to neutralize the randomly appearing hostile
#spaceships by the help of a beam gun, otherwise the red
#objects will shoot it down. The beam gun has a bursting charge
#that explodes at the very end of the beam (symbolized by the end of the white line).
#This has to be inside the hostile objects and strictly not only on the edge
#of them, otherwise the shoots are nugatory and the spaceship of the AI will lose.
#AI is a bit faster than the enemy, so the AI to shoot first each time.
#Once a red object is shot down, a new one will be appearing randomly
#on the map. To make it more complicated for the AI, hostile spaceships will
#become smaller and smaller as the game proceeds. You can make the AI learn
#in the shooting range by setting the number in line 83. The bigger the number
#the more the AI learns and the closer it gets to be a perfect sharpshooter.
#Have fun! :)

#Andras Komjathy




import numpy as np
import pygame
import random
import time

class NeuralNetwork():

    def __init__(self):

        np.random.seed(1)

        self.synaptic_weights = 2*np.random.random((2,1)) -1

    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def sigmoid_derivatives(self, x):
        return x*(1-x)

    def train(self, training_inputs, training_outputs, training_iterations):

        
        for iteration in range(training_iterations):

            output =  self.think(training_inputs)

            error = training_outputs - output
            adjustments = np.dot(training_inputs.T,error*self.sigmoid_derivatives(output))
            self.synaptic_weights +=adjustments

    def think(self, inputs):

        inputs = inputs.astype(float)
        output = (np.dot(inputs, self.synaptic_weights))

        return output
        

if __name__=="__main__":

    neural_network = NeuralNetwork()

    print('Random synaptic weights: ')
    print(neural_network.synaptic_weights)
    
#The following numbers are the training values for the neural network to learn.
#Basically, the purpose is to teach it to find the very middle of the 'hostile' squares.


    training_inputs = np.array([[0.2,0.1],
                                [0.43,0.26],[0.3,0.5],[0.1,0],[0.4,0.6],[0.7,0.9],[0.3,0.3],[0.9,0.1]])

    training_outputs = np.array([[0.15,0.345,0.4,0.05,0.5,0.8,0.3,0.5]]).T

#The number at the end of the following line shows
#how many iterations the neural network goes through,
#with other words, how much it practices in the 'shooting range'.

    
    neural_network.train(training_inputs, training_outputs,100) 



pygame.init()

white=(255,255,255)
green=(0,255,0)
black=(200,200,150)
red=(255,0,0)
blue=(0,0,255)

display_width=800
display_height=600




gameDisplay=pygame.display.set_mode((800,600))


gameDisplay.fill(black)

#Drawing the green square-shaped spaceship for the AI.

pygame.draw.rect(gameDisplay, green, (375,275,50,50))

add=83
shot_down=-1



print(neural_network.synaptic_weights)

def text_objects(text, font):
    textSurface=font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def win_message_display(text):
    largeText=pygame.font.Font('freesansbold.ttf',115)#Setting size and font.
    TextSurf, TextRect=text_objects("AI wins!", largeText)
    TextRect.center=((400),(300))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(7)



def message_display(text):
    largeText=pygame.font.Font('freesansbold.ttf',115)

    
    
    TextSurf, TextRect=text_objects("AI lost!", largeText)
    TextRect.center=((400),(300))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(7)


def lose():
    time.sleep(0.5)
    message_display("AI lost!")
    
def win():
    win_message_display("AI wins!")

for i in range(33):  
    time.sleep(1)
    a=random.randint(0,717)
    b=random.randint(0,517)
    c=a+add
    d=b+add
    e=200
    f=100

    x=(neural_network.think(np.array([a,c])))
    y=(neural_network.think(np.array([b,d])))

    x1 = list(map(int, x))
    y1 = list(map(int, y))


    strings = [str(integer) for integer in x1]
    a_string = "".join(strings)
    x2 = int(a_string)

    strings = [str(integer) for integer in y1]
    a_string = "".join(strings)
    y2 = int(a_string)

#The spaceships of the enemy will be appearing in random places
#and as the game proceeds they will become smaller and smaller.

    pygame.draw.polygon(gameDisplay, red, ((a,b),(c,b),(c,d),(a,d)))
    
    pygame.display.update()
    time.sleep(0.25)
    pygame.draw.line(gameDisplay, white, (400,300),(x2,y2),(3))
    pygame.display.update()

    if x2>a and c>x2 and y2>b and d>y2:
        pygame.display.update()
        time.sleep(0.25)
        pygame.draw.polygon(gameDisplay, black, ((a,b),(c,b),(c,d),(a,d)))
        pygame.draw.line(gameDisplay, black, (400,300),(x2,y2),(3))
        pygame.draw.rect(gameDisplay, green, (375,275,50,50))
    else:
        time.sleep(0.75)
        pygame.draw.line(gameDisplay, red, (a,b),(400,300),(3))
        pygame.display.update()
        lose()
        pygame.quit()

#The enemy will become smaller and smaller
        
    add=add-3

#There will be a counter that shows the hostile
#objects shot down.

    shot_down=shot_down+1

    print("Shot down:")
    print(shot_down)

    if add<0:
        win()
        pygame.quit()

    
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()
