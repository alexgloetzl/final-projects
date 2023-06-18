function [C, sigma] = dataset3Params(X, y, Xval, yval)
%DATASET3PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = DATASET3PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
%C = 1;
%sigma = 0.3;

parameter_values = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30];
p_size = length(parameter_values);
errors = zeros(1,p_size^2);
%counter = 1;
for i = 1:p_size
    for j = 1:p_size
        C = parameter_values(i);
        sigma = parameter_values(j);
        model= svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma));
        predictions = svmPredict(model, Xval);
        errors(j+(i-1)*p_size) = mean(double(predictions ~= yval));
        %counter = counter + 1;
    end 
end
%errors
[~,ind] = min(errors);
C_ind = fix(ind/p_size);
sigma_ind = mod(ind,p_size);
C = parameter_values(C_ind);
sigma = parameter_values(sigma_ind);
%C
%sigma
%[C_ind, sigma_ind]
end
% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%
% =========================================================================


