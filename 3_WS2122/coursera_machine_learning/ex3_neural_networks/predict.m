function p = predict(Theta1, Theta2, X)
%PREDICT Predict the label of an input given a trained neural network
%   p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
%   trained weights of a neural network (Theta1, Theta2)

% Useful values
m = size(X, 1);
num_labels = size(Theta2, 1);

% You need to return the following variables correctly 
p = zeros(size(X, 1), 1);

X = [ones(size(X,1),1), X];
z2 = Theta1 * X';
a2 = sigmoid(z2);

a2 = [ones(1,size(a2,2)); a2]; %für oberste zeile werden "einser" eingeführt
z3 = Theta2 * a2;
a3 = sigmoid(z3);

[~,p0] = max(a3); %~ ist scheinbar wichtig. nur [,p0] geht nicht
p = p0';
% ====================== YOUR CODE HERE ======================
% Instructions: Complete the following code to make predictions using
%               your learned neural network. You should set p to a 
%               vector containing labels between 1 to num_labels.
%
% Hint: The max function might come in useful. In particular, the max
%       function can also return the index of the max element, for more
%       information see 'help max'. If your examples are in rows, then, you
%       can use max(A, [], 2) to obtain the max for each row.
%









% =========================================================================


end
