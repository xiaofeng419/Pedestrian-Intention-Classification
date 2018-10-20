%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%SampleFromFile.m           %
%Author: Liu Yang           %
%Mail: liuyeung@stanford.edu%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function SampleFromFile(vbbPath, seqPath, sampleImgDir, sampleBBDir, vidID, pedID, startFrameID, endFrameID, tag)
  vb = vbb('vbbLoad', vbbPath);
  sq = seqIo(seqPath, 'reader');
  id = getPedVbbID(vb, pedID); 
  if id == 0
      sq.close();
      return;
  end
  bbox = vbb('getVal', vb, id, 'pos', startFrameID, endFrameID);
  flag = zeros(1, length(bbox));
  flag(1) = 1;
  idx = 1;
  %eliminate heavily overlap bbox
  for i = 2:length(bbox)
      if(computeOverlapRatio(bbox(i,:), bbox(idx, :)) < 0.9)
         flag(i) = 1;
         idx = i;
      end
  end
  keepIdx = find(flag == 1);
  for i = 1:length(keepIdx)
    if(bbox(keepIdx(i), 3) < 40 || bbox(keepIdx(i), 4) < 40)
        continue;
    end
    imgName = [vidID '_' pedID '_I' int2str2(i,2) '.png'];
    imgPath = fullfile(sampleImgDir, imgName);
    annName = [vidID '_' pedID '_B' int2str2(i,2) '.txt'];
    annPath = fullfile(sampleBBDir, annName);
    sq.seek(keepIdx(i)+startFrameID-1);
    I = sq.getframeb();
    imf = fopen(imgPath, 'w');
    fwrite(imf, I);
    fclose(imf);
    annContent = sprintf("%s, %d, %d, %d, %d, %s, %s", pedID, ...
                         round(bbox(keepIdx(i), 1)),round(bbox(keepIdx(i), 2)), round(bbox(keepIdx(i), 3)), round(bbox(keepIdx(i), 4)), ...
                         tag, imgName);
    anf = fopen(annPath, 'w');
    fwrite(anf, annContent);
    fclose(anf);
  end 
  sq.close();
end

function [id] = getPedVbbID(vb, pedID)
  ids = vb.objLbl;
  for i = 1:length(ids)
     if strcmp(pedID, ids{i})
        id = i;
        return;
     end
  end
  id = 0;
end

function [ratio] = computeOverlapRatio(rec1, rec2)
  x0 = rec2(1) - rec1(1);
  y0 = rec2(2) - rec1(2);
  w0 = max(0, x0 + rec2(3));
  h0 = max(0, y0 + rec2(4));
  w1 = min(w0, rec1(3));
  h1 = min(h0, rec1(4));
  ratio = w1*h1/(rec1(3)*rec1(4));
end