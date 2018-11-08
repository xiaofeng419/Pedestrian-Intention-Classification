%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%SampleFromFile.m           %
%Author: Liu Yang           %
%Mail: liuyeung@stanford.edu%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [ids] = GetPedVbbID(vb, pedID)
  flags = zeros(1, length(vb.objLbl));
  for i = 1:length(vb.objLbl)
      if strcmp(vb.objLbl{i}, pedID)
          flags(i) = 1;
      else
          if ~isempty(regexp(vb.objLbl{i}, ['^' pedID '_p[0-9]'], 'match'))
              flags(i) = 1; 
          end
      end
  end
  ids = find(flags);
%   if length(ids) > 1
%      a = 1; 
%   end
end