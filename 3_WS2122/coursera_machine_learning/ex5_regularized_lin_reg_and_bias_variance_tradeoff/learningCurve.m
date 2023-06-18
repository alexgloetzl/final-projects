function [error_train, error_val] = ...
    learningCurve(X, y, Xval, yval, lambda)
%LEARNINGCURVE Generates the train and cross validation set errors needed 
%to plot a learning curve
%   [error_train, error_val] = ...
%       LEARNINGCURVE(X, y, Xval, yval, lambda) returns the train and
%       cross validation set errors for a learning curve. In particular, 
%       it returns two vectors of the same length - error_train and 
%       error_val. Then, error_train(i) contains the training error for
%       i examples (and similarly for error_val(i)).
%
%   In this function, you will compute the train and test errors for
%   dataset sizes from 1 up to m. In practice, when working with larger
%   datasets, you might want to do this in larger intervals.
%
% Number of training examples
m = size(X, 1);
% You need to return these values correctly
error_train = zeros(m, 1);
error_val   = zeros(m, 1);

% exercise 2: Learning curves (non-optional)
% for i = 1:m
%     theta_i = trainLinearReg(X(1:i,:),y(1:i),lambda);
%     %prediction = X(1:i,:) * theta_i - y(1:i);
%     %error_train(i) = (1/2*m) * (prediction' * prediction);
%     [error_train(i), ~] = linearRegCostFunction(X(1:i,:),y(1:i),theta_i,0); 
% 
%     %prediction_cv = X * theta_i - y;
%     %error_cv(i) = (1/2*m) * (prediction_cv' * prediction_cv);
%     [error_val(i), ~] = linearRegCostFunction(Xval,yval,theta_i,0);
% end

%exercise 3.5 (optional): learning curves with randomly selected samples 
%(average over 50 samples)
N_avg = 3;
%m_val = size(Xval, 1);
for i = 1:m
    error_train_N = zeros(1,N_avg);
    error_val_N = zeros(1,N_avg);
    for t = 1:N_avg
        rows_train = randsample(m,i);
        %rows_val = randsample(m_val,i);
        theta_i = trainLinearReg(X(rows_train,:),y(rows_train),lambda);

        [error_train_N(t), ~] = linearRegCostFunction(X(rows_train,:),y(rows_train),theta_i,0); 
        
        [error_val_N(t), ~] = linearRegCostFunction(Xval,yval,theta_i,0);
    end
    error_train(i) = mean(error_train_N);
    error_val(i) = mean(error_val_N);
end

end
% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return training errors in 
%               error_train and the cross validation errors in error_val. 
%               i.e., error_train(i) and 
%               error_val(i) should give you the errors
%               obtained after training on i examples.
%
% Note: You should evaluate the training error on the first i training
%       examples (i.e., X(1:i, :) and y(1:i)).
%
%       For the cross-validation error, you should instead evaluate on
%       the _entire_ cross validation set (Xval and yval).
%
% Note: If you are using your cost function (linearRegCostFunction)
%       to compute the training and cross validation error, you should 
%       call the function with the lambda argument set to 0. 
%       Do note that you will still need to use lambda when running
%       the training to obtain the theta parameters.
%
% Hint: You can loop over the examples with the following:
%
%       for i = 1:m
%           % Compute train/cross validation errors using training examples 
%           % X(1:i, :) and y(1:i), storing the result in 
%           % error_train(i) and error_val(i)
%           ....
%           
%       end
%
% ---------------------- Sample Solution ----------------------
% -------------------------------------------------------------
% =========================================================================
