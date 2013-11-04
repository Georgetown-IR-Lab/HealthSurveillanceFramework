package healthSurveillanceFramework.fileFormats;

import java.util.ArrayList;
import java.util.Map;

public class DocMetadata extends JsonFile {
    private Map<String, Map<String, String>> metadata;

    @SuppressWarnings("unchecked")
    public void loadJson(String filename) {
        String json = readFile(filename);
        metadata = (Map<String, Map<String, String>>) parser.parseJson(json);
    }

    public void writeJson(String filename) {
         String json = generator.generateJson(metadata);

        // quick-json encloses the data in an outside array
        // TODO figure out a better way to handle this
        json = json.substring(1, json.length() - 1);

        writeFile(json, filename);
    }

    public Map<String, Map<String, String>> getMetadata() {
        return metadata;
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("usage: <DocumentMetadata file>");
            System.exit(1);
        }

        DocMetadata dm = new DocMetadata();
        dm.loadJson(args[0]);

        System.out.println("document ids found in '" + args[0] + "':");
        for (String docid : dm.getMetadata().keySet())
            System.out.println("\t" + docid);
    }

}
