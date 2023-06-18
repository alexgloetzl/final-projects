function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)

%die vectorizierte form ist deutlich langsamer als die nicht-vetorizierte
%form. keine ahnung warum. vielleicht weil myY([mx10]-matrix) zu viel
%speicher frisst?

%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices. 
% 
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
% for our 2 layer neural network
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

% Setup some useful variables
m = size(X, 1);
         
% You need to return the following variables correctly 
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));

X_add = [ones(size(X,1),1), X];
z2 = Theta1 * X_add';
a2 = sigmoid(z2); % size = 25xm

%a2 = [ones(1,size(a2,2)); a2]; %für oberste zeile werden "einser"
%eingeführt. In zeile darunter dann: z3 = Theta2 * a2;
a2_add = [ones(size(a2,2),1), a2']; %einser for 1. spalte eingeführt % size(a2) = (25+1)xm
z3 = Theta2 * a2_add';
a3 = sigmoid(z3);


%Cost function (v1) which is a bit more vectorized:
myY = 1:num_labels == y;
%size(myY)
%size(a3)
J_m = 0;
for c = 1:m
    J_m = J_m + (-myY(c,:)*log(a3(:,c)) - (1-myY(c,:))*log(1-a3(:,c)));
end
theta1_squared = Theta1(:,2:end).*Theta1(:,2:end);
theta2_squared = Theta2(:,2:end).*Theta2(:,2:end);
J_theta = lambda/(2*m) * ( sum(theta1_squared(:))+sum(theta2_squared(:)) );
J = (1/m) * J_m + J_theta;

% Cost function (v2) which is a bit less vectorized:
% J_m = 0;
% %sprintf("m: %d", m)
% for c = 1:m
%     y_ind = y(c);
%     myY = [zeros(num_labels,1)];
%     myY(y_ind) = 1;
%     %myY
%     %pred = sigmoid(a3() * theta);
%     J_m = J_m + (-myY'*log(a3(:,c)) - (1-myY)'*log(1-a3(:,c))); %+ lambda/(2*m).*(theta(2:end)'*theta(2:end));
% end
% theta1_squared = Theta1(:,2:end).*Theta1(:,2:end);
% theta2_squared = Theta2(:,2:end).*Theta2(:,2:end);
% J_theta = lambda/(2*m) * ( sum(theta1_squared(:))+sum(theta2_squared(:)) );
% 
% J = (1/m) * J_m + J_theta;


%grad (v1) which is a bit more vectorized. using myY from above
for t = 1:m
    delta3 = a3(:,t) - myY(t,:)';
    delta2 = (Theta2'*delta3);
    delta2 = delta2(2:end).*sigmoidGradient(z2(:,t));
    Theta1_grad = Theta1_grad + delta2*X_add(t,:);
    Theta2_grad = Theta2_grad + delta3*a2_add(t,:);
end

%grad (v2) which is a bit less vectorized
% for t = 1:m
%     y_ind = y(t);
%     myY = [zeros(num_labels,1)];
%     myY(y_ind) = 1;
%     %size(myY)
%     delta3 = a3(:,t) - myY;
%     %size(Theta2)
%     %size(delta3)
%     delta2 = (Theta2'*delta3); %size(delta2) = (26x10)*(10x1)=(26x1)
%     %size(delta2)
%     %size(sigmoidGradient(z2))
%     delta2 = delta2(2:end).*sigmoidGradient(z2(:,t)); %size(delta2) = (25x1)
%     %size(Theta1_grad)
%     %size(delta2)
%     %size(X_add(t,:))
%     %size(a2_add)
%     Theta1_grad = Theta1_grad + delta2*X_add(t,:);
%     Theta2_grad = Theta2_grad + delta3*a2_add(t,:);
% end

Theta1_grad = (1/m) * Theta1_grad;
Theta2_grad = (1/m) * Theta2_grad;
%fprintf("hallo!")
Theta1_grad(:,2:end) = Theta1_grad(:,2:end) + (lambda/m) .* Theta1(:,2:end);
Theta2_grad(:,2:end) = Theta2_grad(:,2:end) + (lambda/m) .* Theta2(:,2:end);

%unroll gradient.
grad = [Theta1_grad(:); Theta2_grad(:)];

end
% ====================== YOUR CODE HERE ======================
% Instructions: You should complete the code by working through the
%               following parts.
%
% Part 1: Feedforward the neural network and return the cost in the
%         variable J. After implementing Part 1, you can verify that your
%         cost function computation is correct by verifying the cost
%         computed in ex4.m
%
% Part 2: Implement the backpropagation algorithm to compute the gradients
%         Theta1_grad and Theta2_grad. You should return the partial derivatives of
%         the cost function with respect to Theta1 and Theta2 in Theta1_grad and
%         Theta2_grad, respectively. After implementing Part 2, you can check
%         that your implementation is correct by running checkNNGradients
%
%         Note: The vector y passed into the function is a vector of labels
%               containing values from 1..K. You need to map this vector into a 
%               binary vector of 1's and 0's to be used with the neural network
%               cost function.
%
%         Hint: We recommend implementing backpropagation using a for-loop
%               over the training examples if you are implementing it for the 
%               first time.
%
% Part 3: Implement regularization with the cost function and gradients.
%
%         Hint: You can implement this around the code for
%               backpropagation. That is, you can compute the gradients for
%               the regularization separately and then add them to Theta1_grad
%               and Theta2_grad from Part 2.
%
% -------------------------------------------------------------

% =========================================================================