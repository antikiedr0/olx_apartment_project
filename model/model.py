import torch
import torch.nn as nn
from prepare_data import load_data

class Model(nn.Module):

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(22, 64),
            nn.ReLU(),
            nn.Dropout(0.2),     # randomly drops 20% of neurons to prevent overfitting
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        return self.layers(x)


def train(model, X_train, y_train, X_test, y_test, epochs=500):
    # mean squared error — standard loss for regression
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()

        predictions = model(X_train)
        loss = loss_fn(predictions, y_train)

        loss.backward()
        optimizer.step()

        if (epoch + 1) % 100 == 0:
            model.eval()
            with torch.no_grad():
                test_loss = loss_fn(model(X_test), y_test)
            # if test loss is much higher than train loss — model is overfitting
            print(f"Epoch {epoch + 1}/{epochs} | Train: {loss.item():.3f} | Test: {test_loss.item():.3f}")


def evaluate(model, X_test, y_test, y_mean, y_std):
    model.eval()
    with torch.no_grad():
        predictions = model(X_test)
        # denormalize to get real PLN/m² values
        predictions = predictions * y_std + y_mean
        y_real = y_test * y_std + y_mean
        mae = (predictions - y_real).abs().mean().item()
        print(f"Sredni blad: {mae:.0f} PLN/m²")


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, mean, std, y_mean, y_std = load_data()

    model = Model()
    train(model, X_train, y_train, X_test, y_test)
    evaluate(model, X_test, y_test, y_mean, y_std)

    torch.save(model.state_dict(), 'model/model.pth')
    print("Model zapisany do model/model.pth")
