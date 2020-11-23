function masks = OtsuN(dataset, ss, cNum, img, outputDir)
    clusters = OtsuNCore(img, cNum);
    
    masks = SortMasks(dataset, ss, cNum, img, clusters, outputDir);
end

