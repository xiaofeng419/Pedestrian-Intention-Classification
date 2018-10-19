%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%ParseJAADBehAnnote.m       %
%Author: Liu Yang           %
%Mail: liuyeung@stanford.edu%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [annotate] = ParseJAADBehAnnote(path)
  fileID = fopen(path);
  fc = textscan(fileID, '%s %s %d %s %s %s %s %s %d %s %s %d', 'Delimiter', ',');
  annotate.vidID = fc{1};
  annotate.pedID = fc{2};
  annotate.groupSize = fc{3}; 
  annotate.motionDirection = fc{4};
  annotate.designated = fc{5};
  annotate.signalized = fc{6};
  annotate.gender = fc{7};
  annotate.age = fc{8};
  annotate.numLanes = fc{9};
  annotate.trafficDirection = fc{10};
  annotate.intersection = fc{11};
  annotate.crossing = fc{12};
  fclose(fileID);
end