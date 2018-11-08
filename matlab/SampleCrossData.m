%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%SampleCrossData.m          %
%Author: Liu Yang           %
%Mail: liuyeung@stanford.edu%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Sample data for the pedestrian crossing case     %
%pedID: pedestrian ID                             %
%vidID: video ID in which the pedestrian appear   %
%behAnn: behavior note                            %
%vbbRoot: path to the .vbb files                  %
%seqRoot: path to the .seq files                  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function SampleCrossData(attAnn, behAnn, vbbRoot, sampleRoot)
  crossIdx = find(attAnn.crossing == 1);
  vpID = [attAnn.vidID(crossIdx), attAnn.pedID(crossIdx)];
  crossActID = CheckCrossState(behAnn, vpID);
  crossDir = fullfile(sampleRoot, 'cross');

  if ~exist(crossDir, 'dir')
      mkdir(crossDir);
  end

  for i = 1:length(vpID)
    vidID = vpID{i,1};
    pedInfo = behAnn(vidID);
    pedID = vpID{i, 2};
    pAct = pedInfo.(pedID);
    cid = crossActID(i);
    startFrameID = pAct(cid).start_frame - 5;
    endFrameID = pAct(cid).end_frame + 5;
    vbbPath = fullfile(vbbRoot, [vpID{i,1} '.vbb']);
    vb = vbb('vbbLoad', vbbPath);
    ids = GetPedVbbID(vb, pedID);
    [id, startFrameID, endFrameID] = checkConsistency(vb, ids, startFrameID, endFrameID);
    SampleFromFile(vb, crossDir, vidID, pedID, id, startFrameID, endFrameID, 'cross');
  end
end

function [crossMap] = CheckCrossState(behAnn, vpID)
  sampleNum = length(vpID);
  crossMap = zeros(1, sampleNum);
  for i = 1:sampleNum
      videoID = vpID{i, 1};
      pedID = vpID{i, 2};
      pedInfo = behAnn(videoID);
      personAct = pedInfo.(pedID);
      for j = length(personAct):-1:1
          if strcmp(personAct(j).id, 'crossing')
              crossMap(i) = j;
              break;
          end
      end
  end
end

function [id, sf, ef] = checkConsistency(vb, ids, startFrameID, endFrameID)
  for i = 1:length(ids)
      action = vbb('get', vb, ids(i));
      left = max(startFrameID, action.str);
      right = min(endFrameID, action.end);
      if((right - left + 1)/(endFrameID - startFrameID + 1) > 0.7)
         id = ids(i);
         sf = left;
         ef = right;
         break;
      end
  end
end













