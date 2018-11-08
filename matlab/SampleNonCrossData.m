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

function SampleNonCrossData(attAnn, vbbRoot, sampleRoot)
  ncIdx = find(attAnn.crossing == 0);
  plusIdx = find(attAnn.crossing == -1);
  ncIdx = [ncIdx;plusIdx];
  vpID = [attAnn.vidID(ncIdx), attAnn.pedID(ncIdx)];
  ncDir = fullfile(sampleRoot, 'non-cross');

  if ~exist(ncDir, 'dir')
      mkdir(ncDir);
  end
  
  for i = 1:length(vpID)
    vidID = vpID{i,1};
    pedID = vpID{i, 2};
    vbbPath = fullfile(vbbRoot, [vpID{i,1} '.vbb']);
    vb = vbb('vbbLoad', vbbPath);
    ids = GetPedVbbID(vb, pedID);
    if length(ids) > 1
        test = 1;
    end
    for j = 1:length(ids)
        action = vbb('get', vb, ids(j));
        SampleFromFile(vb, ncDir, vidID, pedID, ids(j), action.str, action.end, 'non-cross');
    end
  end
end