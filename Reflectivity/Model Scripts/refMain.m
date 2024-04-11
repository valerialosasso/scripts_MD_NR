%% Fit to 20 mN data.... 
%Requtres that the RAT toolbox should be present and initialised
global monolayerNDs

% Load in the processed Number Densities...
% (created with 'groupDists.m')
monolayerNDs = load('monolayerNDs.mat');
monolayerNDs = monolayerNDs.monolayerNDs;

% Plot the distributions...
figure(1); clf
plot(monolayerNDs.z,monolayerNDs.allDists)

% make the RAT model...
problem = twenty_mN_script();

% Make a controls block..
controls = controlsClass();

% Set for Differential evolution..
controls.procedure = 'de';
controls.parallel = 'contrasts';

% Run the RAT toolbox..
[problem,results] = RAT(problem,controls);

% Plot the results...
plotRefSLD(problem,results);









