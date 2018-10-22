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
  plusIdx = find(attAnn.crossing == -1);
  ncIdx = [ncIdx;plusIdx];
  vpID = [attAnn.vidID(ncIdx), attAnn.pedID(ncIdx)];
  ncDir = fullfile(sampleRoot, 'non-cross');
  sampleImgDir = fullfile(ncDir, 'image');
  sampleBBDir = fullfile(ncDir, 'bbox');
  if ~exist(ncDir, 'dir')
      mkdir(ncDir);
      mkdir(sampleImgDir);
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
    startFrameID = frameID;%max(pAct(1).start_frame, frameID-10);
    endFrameID = pAct(actNum).end_frame;%min(pAct(cid).end_frame, frameID+30);
    vbbPath = fullfile(vbbRoot, [vpID{i,1} '.vbb']);
    seqPath = fullfile(seqRoot, [vpID{i,1} '.seq']);
    SampleFromFile(vbbPath, seqPath, sampleImgDir, sampleBBDir, vidID, pedID, startFrameID, endFrameID, 'non-cross');
  end
end