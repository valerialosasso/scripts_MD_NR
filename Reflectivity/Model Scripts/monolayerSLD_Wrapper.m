function [SLD,subRough] = monolayerSLD_20mN_Wrapper(params,bulkIn,bulkOut,contrast)

global monolayerNDs

monolayer = monolayerNDs;

% Set deuteration flags - 1 is Deuterated, 0 is Hydrogenated.
% The order of these should match the order of the contrasts in the
% RAT model.
%        chain   Head
D_Flags = [0      1;
           0      1;
           1      0;
           1      0;
           1      1;
           1      1;
           0      0];
             
thisDFlag = D_Flags(contrast,:);
             
SLD = monolayerSLD(params,bulkIn,bulkOut,monolayer,thisDFlag,contrast,0);
subRough = params(1);

end
