
function problem = twenty_mN_script()

%% DSPC Monlayers Data fit With MD Simulations (including water volume fit)

% Start by making a projectClass. 
problem = projectClass();
problem.experimentName = '20mN DSPC / MD';
problem.modelType = 'Custom XY';

% Allow the use of Bayesian priors..
problem.setUsePriors(true);

% Set the range of the default scalefactor
problem.setScalefactor(1,'min',0.15,'max',0.25);

%% 
% The data has been measured against D2O and ACMW, so we need bulkOut and Backgrounds 
% for these...

problem.setBackgroundParam(1,'name','D2O BacksPar','fit',true);
problem.setBackgroundName(1,'D2O Background');
problem.setBackground(1,'Value1','D2O BacksPar');

problem.addBackgroundParam('ACMW BacksPar',1e-7,1e-6,1e-5,true);
problem.addBackground('ACMW Background','constant','ACMW BacksPar');

% We also need a bulk out for the ACMW....
problem.addBulkOut('SLD ACMW',-1e-7,0,1e-6);

problem.setBulkOut(1,'fit',true);
problem.setBulkOut(2,'fit',true);
problem.setScalefactor(1,'fit',true,'min',0.15,'max',0.25);

%% 
% Set priors for the water SLD's....
problem.bulkOut.setPrior(1,'gaussian',6.35e-6,1e-7);
problem.bulkOut.setPrior(2,'gaussian',0,1e-7);


%% 
% load in and add the data.....
this = fileparts(mfilename('fullpath'));
dataPath = fullfile(this,'..','Datafiles');

dataFileNames = {'d13acmw20.dat','d13d2o20.dat','d70acmw20.dat',...
    'd70d2o20.dat','d83acmw20.dat','d83d2o20.dat','hd2o20.dat'};

for i = 1:length(dataFileNames)
   thisDataFileName = dataFileNames{i};
   thisDataFile = dlmread(fullfile(dataPath,thisDataFileName));
   problem.addData(thisDataFileName,thisDataFile);
end

%% 
% Add the custom model file..

problem.addCustomFile('DSPC Monolayer MD','monolayerSLD_Wrapper.m','matlab','pwd');

%% 
% Make the contrasts....

problem.addContrast('name','d13 ACMW 20',...
    'background','ACMW Background',...
    'resolution','Resolution 1',...
    'scalefactor', 'Scalefactor 1',...
    'BulkOut', 'SLD ACMW',...        % This is bulk out ('Nb Subs')
    'BulkIn', 'SLD Air',...        % This is bulk in ('Nb Air')
    'data', 'd13acmw20.dat');
problem.setContrastModel(1,'DSPC Monolayer MD');

problem.addContrast('name','d13 D2O 20',...
    'background','D2O Background',...
    'resolution','Resolution 1',...
    'scalefactor', 'Scalefactor 1',...
    'BulkOut', 'SLD D2O',...        % This is bulk out ('Nb Subs')
    'BulkIn', 'SLD Air',...        % This is bulk in ('Nb Air')
    'data', 'd13d2o20.dat');
problem.setContrastModel(2,'DSPC Monolayer MD');

problem.addContrast('name','d70 ACMW 20',...
    'background','ACMW Background',...
    'resolution','Resolution 1',...
    'scalefactor', 'Scalefactor 1',...
    'BulkOut', 'SLD ACMW',...        % This is bulk out ('Nb Subs')
    'BulkIn', 'SLD Air',...        % This is bulk in ('Nb Air')
    'data', 'd70acmw20.dat');
problem.setContrastModel(3,'DSPC Monolayer MD');

problem.addContrast('name','d70 D2O 20',...
    'background','D2O Background',...
    'resolution','Resolution 1',...
    'scalefactor', 'Scalefactor 1',...
    'BulkOut', 'SLD D2O',...        % This is bulk out ('Nb Subs')
    'BulkIn', 'SLD Air',...        % This is bulk in ('Nb Air')
    'data', 'd70d2o20.dat');
problem.setContrastModel(4,'DSPC Monolayer MD');

problem.addContrast('name','d83 ACMW 20',...
    'background','ACMW Background',...
    'resolution','Resolution 1',...
    'scalefactor', 'Scalefactor 1',...
    'BulkOut', 'SLD ACMW',...        % This is bulk out ('Nb Subs')
    'BulkIn', 'SLD Air',...        % This is bulk in ('Nb Air')
    'data', 'd83acmw20.dat');
problem.setContrastModel(5,'DSPC Monolayer MD');

problem.addContrast('name','d83 D2O 20',...
    'background','D2O Background',...
    'resolution','Resolution 1',...
    'scalefactor', 'Scalefactor 1',...
    'BulkOut', 'SLD D2O',...        % This is bulk out ('Nb Subs')
    'BulkIn', 'SLD Air',...        % This is bulk in ('Nb Air')
    'data', 'd83d2o20.dat');
problem.setContrastModel(6,'DSPC Monolayer MD');

problem.addContrast('name','h D2O 20',...
    'background','D2O Background',...
    'resolution','Resolution 1',...
    'scalefactor', 'Scalefactor 1',...
    'BulkOut', 'SLD D2O',...        % This is bulk out ('Nb Subs')
    'BulkIn', 'SLD Air',...        % This is bulk in ('Nb Air')
    'data', 'hd2o20.dat');
problem.setContrastModel(7,'DSPC Monolayer MD');


end