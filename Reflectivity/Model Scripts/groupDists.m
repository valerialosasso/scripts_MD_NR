function monolayer = groupDists(simPath)

%% Group the ND distributions (from the Python scripts) fro reflectivity analysis

% Load in the simulations....
c = dlmread(fullfile(simPath,'carbon.dat')); c = flipud(c); c = c(1:end-1,:);
n = dlmread(fullfile(simPath,'nitrogen.dat')); n = flipud(n); n = n(1:end-1,:);
p = dlmread(fullfile(simPath,'phosphorus.dat')); p = flipud(p); p = p(1:end-1,:);
o = dlmread(fullfile(simPath,'oxygen.dat')); o = flipud(o); o = o(1:end-1,:);
h_heads = dlmread(fullfile(simPath,'hydrogen_heads.dat')); h_heads = flipud(h_heads); h_heads = h_heads(1:end-1,:);
h_tails = dlmread(fullfile(simPath,'hydrogen_tails.dat')); h_tails = flipud(h_tails); h_tails = h_tails(1:end-1,:);
h_linker = dlmread(fullfile(simPath,'hydrogen_linker.dat')); h_linker = flipud(h_linker); h_linker = h_linker(1:end-1,:);
h_ch3 = dlmread(fullfile(simPath,'hydrogen_methyl.dat')); h_ch3 = flipud(h_ch3); h_ch3 = h_ch3(1:end-1,:);
water = dlmread(fullfile(simPath,'water.dat')); water = flipud(water); water = water(1:end-1,:);

% Water again doubled up....
%water = water(1:159,:);

% Need to interpolate all the files onto the same x
z = c(:,1);

% This has a 1 A step. Need to make a new z with a smaller step....
z = [z(1):0.1:z(end)];
z = z(:);

% % Centre the z on zero
% z = z + 40; % abs(z(1));

newH_Hy = interp1(h_heads(:,1),h_heads(:,2),z);
newH_Ty = interp1(h_tails(:,1),h_tails(:,2),z);
newH_Ly = interp1(h_linker(:,1),h_linker(:,2),z);
newH_Mey = interp1(h_ch3(:,1),h_ch3(:,2),z);
newNy = interp1(n(:,1),n(:,2),z);
newOy = interp1(o(:,1),o(:,2),z);
newPy = interp1(p(:,1),p(:,2),z);
newH2Oy = interp1(water(:,1),water(:,2),z);
newCy = interp1(c(:,1),c(:,2),z);

allDists = [newH_Hy(:) newH_Ty(:) newH_Ly(:) newH_Mey(:), newNy(:) newOy(:) newPy(:) newCy(:)];% newH2Oy];
for i = 1:size(allDists,2)
    allDists(:,i) = smooth(allDists(:,i));
end
vfWat = newH2Oy; 

% Pad some zeros at the air end..
zPadEnd = z(1) - 0.1;
zPadStart = zPadEnd - 10;
zPad = zPadStart:0.1:zPadEnd;

z = [zPad(:) ; z];

distPad = zeros(length(zPad),size(allDists,2));
allDists = [distPad ; allDists];

watPad = zeros(length(zPad),1);
vfWat = [watPad ; vfWat];

figure(1); clf; hold on
plot(z,allDists);

% Put everything together into an array for saving...
monolayer.z = z;
monolayer.allDists = allDists;
monolayer.vfWat = vfWat;


end

