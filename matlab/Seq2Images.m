%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%ParseJAADBehXML.m          %
%Author: Liu Yang           %
%Mail: liuyeung@stanford.edu%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function Seq2Images(seqDir, imgDir)
  imgDir = fullfile(imgDir, 'images');
  if ~exist(imgDir, 'dir')
      mkdir(imgDir);
  end
  seqList = dir(fullfile(seqDir, '*.seq'));
  for i = 1:length(seqList)
      videoName = seqList(i).name(1:end-4); %remove suffix
      targetImgDir = fullfile(imgDir, videoName);
      if ~exist(targetImgDir, 'dir')
         mkdir(targetImgDir); 
      end
      seqFullPath = fullfile(seqList(i).folder, seqList(i).name);
      seqIo(seqFullPath, 'toImgs', targetImgDir);
      imgList = dir(fullfile(targetImgDir, '*.png'));
      configName = fullfile(targetImgDir, 'imagelist.txt');
      f = fopen(configName, 'w');
      for j = 1:length(imgList)
          fprintf(f, '%s\n', imgList(j).name);
      end
      fclose(f);
  end
end