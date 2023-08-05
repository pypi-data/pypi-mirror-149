# DATA

# data = [[80, 40, 60, 20, 0,0,0,0,0,0,0,0,200]]
MODE_ANIMATION = "max"

barHeight = 0.001
barLabels = ["Pulp Fiction", "Jacky Brown", "The Hateful Eight", "Movie 4", "Movie 5", "Movie 6", "Movie very Long Placeholder 7", "Movie 8", "Movie 9", "Movie 10"]
tickLabels = [0, 10, 20, 30, 40, 50]
graphTitle = 'Title Placeholder'
xAxisTitle, yAxisTitle = "x_title", "y_title"

Gridx, Gridy = 100, 60
labelSize, tickSize, titleSize, axisTitleSize = 1.2, 1.2, 1.8, 1.5
barThick, nsubs = 3, 10
nxlabels, nylabels = len(tickLabels), len(barLabels) # Added this in since not all cases will have the same number of x and y labels
t = nxlabels + nylabels

#Element spacing
step = Gridy/(nylabels + 1)#For the bars
tickStep = Gridx/(nxlabels-1) #For x labelsn
barLocation = [-1*(Gridy/2)+(k*step) for k in range(1, nylabels+1)] #Actual y coords of bars

xLabelHeight = -1*(Gridy/2)-1.4
# labelLocx = -1*(Gridx/2 + 2.6)
labelLocx = -5

LABEL_TIME_LOC = (100,30,1)
CAM_LOC = (50, 0, 170)
GRID_LINE_HEIGHT = 26

# current_max = 20

SPEED_SORT = 20 # frames per position change

FONT = "./assets/fonts/Frutiger.ttf"

# COLOR_PALETTE = ["#fd7f6f", "#7eb0d5", "#b2e061", "#bd7ebe", "#ffb55a", "#ffee65", "#beb9db", "#fdcce5", "#8bd3c7"]
COLOR_PALETTE = ["201e1c","6b6763","56666e","484b6e","8e5798","8c5981","181f27","1c2929","6a3c4b","73609c"]


FPS = 192


DATA = [
    [1,2,5,10,20,2000,10_000],
    [5,6,4,100,1,15,2],
    [2,3,4,5,7,8000,10],
    [2,3,4,5,7,8000,10],
    [2,3,4,5,7,8000,5_000],
    [2,3,4,5,7,8000,10],
    [5,6,4,100,1,15,200],
    [5,10,20,100,1,15,2],
    [5,6,4,100,1,1_000,500],
    [5,6,4,50,1,1_500,4_000],
    ]
