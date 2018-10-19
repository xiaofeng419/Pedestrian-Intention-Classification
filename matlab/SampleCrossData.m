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
  vpID = [behAnn.vidID(crossIdx), behAnn.pedID(crossIdx)];
  crossActID = CheckCrossState(behAnn, vpID);
  sampleImgDir = fullfile(sampleRoot, 'image');
  sampleBBDir = fullfile(sampleRoot, 'bbox');
  if ~exist(sampleImgDir, 'dir')
      mkdir(sampleImgDir);
  end
  if ~exist(sampleBBDir, 'dir')
      mkdir(sampleBBDir);
  end
  for i = 1:length(vpID)
    vidID = vpID{i,1};
    pedInfo = behAnn(vidID);
    pedID = vpID{i, 2};
    pAct = pedInfo.(pedID);
    cid = crossActID(i);
    frameID = pAct(cid).start_frame;
    startFrameID = max(pAct(1).start_frame, frameID-10);
    endFrameID = min(pAct(cid).end_frame, frameID+10);
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
