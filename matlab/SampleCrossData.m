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

function SampleCrossData(attAnn, behAnn, vbbRoot, seqRoot, sampleRoot)
  crossIdx = find(attAnn.crossing == 1);
  vpID = [attAnn.vidID(crossIdx), attAnn.pedID(crossIdx)];
  crossActID = CheckCrossState(behAnn, vpID);
  crossDir = fullfile(sampleRoot, 'cross');
  sampleImgDir = fullfile(crossDir, 'image');
  sampleBBDir = fullfile(crossDir, 'bbox');
  if ~exist(crossDir, 'dir')
      mkdir(crossDir);
      mkdir(sampleImgDir);
      mkdir(sampleBBDir);
  end

  for i = 1:length(vpID)
    vidID = vpID{i,1};
    pedInfo = behAnn(vidID);
    pedID = vpID{i, 2};
    pAct = pedInfo.(pedID);
    cid = crossActID(i);
    frameID = pAct(cid).start_frame;
    startFrameID = frameID; %max(pAct(1).start_frame, frameID-30);
    endFrameID = pAct(cid).end_frame;%min(pAct(cid).end_frame, frameID+10);
    vbbPath = fullfile(vbbRoot, [vpID{i,1} '.vbb']);
    seqPath = fullfile(seqRoot, [vpID{i,1} '.seq']);
    SampleFromFile(vbbPath, seqPath, sampleImgDir, sampleBBDir, vidID, pedID, startFrameID, endFrameID, 'cross');
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
