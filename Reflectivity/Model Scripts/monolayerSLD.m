function monolayerSLD = monolayerSLD(params,bulkIn,bulkOut,monolayer,D_Flag,contrast,debug)
% Calculate DSPC monolayer SLD's based on MD structures.

%debug = 1;  % Optional debug plots...

% First get the distributions out of the main struvture. These are atoms
% per unit volume, so SLD's will be these times SL of relevant atoms..
z = monolayer.z;        % Length axis of distributions...

% Split up the distribution array....
allDists = monolayer.allDists;
H_Heads = allDists(:,1);
H_Tails = allDists(:,2);
H_Link = allDists(:,3);
H_Me = allDists(:,4);
nitrogen = allDists(:,5);
oxygen = allDists(:,6);
phospho = allDists(:,7);
carbon = allDists(:,8);

% Also water volume fraction...
watVF = monolayer.vfWat;

% Extract the parameter from params
substrate_roughness = params(1);
%waterVol = 30.2;
watScale = mean(watVF(end-10:end));

%watVF = watVF .* waterVol;
watVF = watVF ./ watScale;

% Define the neutron b's
bc = 0.6646e-4;     %Carbon
bo = 0.5843e-4;     %Oxygen
bh = -0.3739e-4;	%Hydrogen
bp = 0.513e-4;      %Phosphorus
bn = 0.936e-4;      %Nitrogen
bd = 0.6671e-4;     %Deuterium

% Because the the distributions are ND's, then in each case the SLD is
% given by these times ND.

% Choose the deuteration based on the contrastflags
if D_Flag(1)
    tailHyd = bd;
else
    tailHyd = bh;
end

if D_Flag(2)
    headHyd = bd;
else
    headHyd = bh;
end    

% Convert the atomic distributions to SLD
sldTailHyd = H_Tails .* tailHyd;
sldHeadHyd = H_Heads .* headHyd;
sldMeHyd = H_Me .* tailHyd;
sldLinkHyd = H_Link .* bh;
sldCarbon = carbon .* bc;
sldOxygen = oxygen .* bo;
sldPhospho = phospho .* bp;
sldNitrogen = nitrogen .* bn;

% The water distribution is already volume fraction, so the SLD of this is
% just given by VF times SLD of the bulk out...
sldWater = watVF .* bulkOut(contrast);

% Add everything up to get the final SLD....
totSLD = sldTailHyd + sldHeadHyd + sldLinkHyd + sldMeHyd + sldCarbon + sldOxygen + sldPhospho...
    + sldNitrogen + sldWater;


% Now do the roughness convolution. To do this we need to make a centred
% set of distributions which are mainly symmetrical for the convolution to
% work properly - essentially we need it to be zero at both ends.
zLength = length(z);
zFlip = -flipud(z);
totSLDFlip = flipud(totSLD);

zFull = [z ; zFlip];
sldFull = [totSLD ; totSLDFlip];

fullSLD = [zFull(:) sldFull(:)];

if debug
        figure(4); clf; hold on;
        plot(fullSLD(:,1),fullSLD(:,2));
        
end


filter = Gaussian(zFull,0,1,substrate_roughness);
filter = [zFull(:),filter(:)];

% Now do the convolution...
convMonolayer = sld_convolute(fullSLD,filter); 

% Trim this back to the original size, ahs shift to start at zero....
convMonolayer = convMonolayer(1:zLength,:);
convMonolayer(:,1) = convMonolayer(:,1) + abs(convMonolayer(1,1));

monolayerSLD = convMonolayer; % [z(:) convMonolayer(:,2)];

if debug
    figure(3); clf; hold on; subplot(2,1,1);
    plot(monolayerSLD(:,1),monolayerSLD(:,2));

    subplot(2,1,2);
    plot(monolayerSLD(:,1),allDists);
end

end