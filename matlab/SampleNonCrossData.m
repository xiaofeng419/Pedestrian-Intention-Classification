%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%SampleNonCrossData.m       %
%Author: Liu Yang           %
%Mail: liuyeung@stanford.edu%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Sample data for the pedestrian non-crossing case     %
%pedID: pedestrian ID                                 %
%vidID: video ID in which the pedestrian appear       %
%behAnn: behavior note                                %
%vbbRoot: path to the .vbb files                      %
%seqRoot: path to the .seq files                      %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function SampleNonCrossData(attAnn, behAnn, vbbRoot, seqRoot, sampleRoot)
  ncIdx = find(attAnn.crossing == 0);
  vpID = [behAnn.vidID(ncIdx), behAnn.pedID(ncIdx)];
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
    actNum = length(pAct);
    cid = round(actNum/2);
    frameID = pAct(cid).start_frame;
    startFrameID = max(pAct(1).start_frame, frameID-10);
    endFrameID = min(pAct(cid).end_frame, frameID+10);
    vbbPath = fullfile(vbbRoot, [vpID{i,1} '.vbb']);
    seqPath = fullfile(seqRoot, [vpID{i,1} '.seq']);
    SampleFromFile(vbbPath, seqPath, sampleImgDir, sampleBBDir, vidID, pedID, startFrameID, endFrameID, 'non-cross');
  end
end