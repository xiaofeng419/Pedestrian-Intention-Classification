%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%SampleFromFile.m           %
%Author: Liu Yang           %
%Mail: liuyeung@stanford.edu%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function SampleFromFile(vb, sampleDir, vidID, pedID, vbbID, startFrameID, endFrameID, tag)
  %bounding box is assured existing for frame in range [startFrameID, endFrameID]
  bbox = vbb('getVal', vb, vbbID, 'pos', startFrameID, endFrameID);
  frameNum = length(bbox);
  sampleLen = 20;
  for i = 1:sampleLen:frameNum
    segID = ceil(i/sampleLen);
    left = i;
    right = min(left + sampleLen - 1, frameNum);
    segName = [vidID '_' pedID '_p' int2str2(vbbID, 2) '_I' int2str2(segID,2) '.txt'];
    segPath = fullfile(sampleDir, segName);
    f = fopen(segPath, 'wt');
    fprintf(f, '%s, %s, %d, %s\r\n', vidID, pedID, right - left + 1, tag);
    for j = left:right
        rawFrameID = startFrameID + j - 1;
        fprintf(f, '%d, %d, %d, %d, %d\r\n', rawFrameID, round(bbox(j, 1)), round(bbox(j, 2)), round(bbox(j, 3)), round(bbox(j, 4)));
    end
    fclose(f);
  end
end

