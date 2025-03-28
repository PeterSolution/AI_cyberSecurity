import torch
import torch.nn as nn
import torch.optim as optim
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(1, 30)
        self.fc2 = nn.Linear(30, 1)

    def saveModel(self,model):
        torch.save(model.state_dict(), "model.pth")
        print("Model zapisany do model.pth")

    def LearnModelAmountOfTime(self,model,amount,csv_data,targetOutput):
        learning=optim.SGD(model.parameters(),lr=0.01)
        middleSqrError=nn.MSELoss()
        for epoch in range(amount):
            learning.zero_grad()
            output=model(csv_data)
            loss=middleSqrError(output,targetOutput)
            loss.backward()
            learning.step()
        torch.save(model.state_dict(),"model.pth")
        return model

    def LearnModelUntilErrorLess(self,model,lesserror,csv_data,targetOutput):
        learning=optim.SGD(model.parameters(),lr=0.01)
        middleSqrError=nn.MSELoss()
        loss=1000000
        while loss>lesserror:
            learning.zero_grad()
            output=model(csv_data)
            loss=middleSqrError(output,targetOutput)
            loss.backward()
            learning.step()
        torch.save(model.state_dict(),"model.pth")
        return model

    def LoadModel(self):
        model=NeuralNetwork()
        model.load_state_dict(torch.load("model.pth"))
        model.eval()
        return model