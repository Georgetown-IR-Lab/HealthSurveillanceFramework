package healthSurveillanceFramework.fileFormats;

import java.util.ArrayList;
import java.util.Map;

public class Documents extends JsonFile {
    private Map<String, String> docs;

    @SuppressWarnings("unchecked")
    public void loadJson(String filename) {
        String json = readFile(filename);
        docs = (Map<String, String>) parser.parseJson(json);
    }

    public void writeJson(String filename) {
         String json = generator.generateJson(docs);

        // quick-json encloses the data in an outside array
        // TODO figure out a better way to handle this
        json = json.substring(1, json.length() - 1);

        writeFile(json, filename);
    }

    public Map<String, String> getDocuments() {
        return docs;
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("usage: <Documents file>");
            System.exit(1);
        }

        Documents d = new Documents();
        d.loadJson(args[0]);

        System.out.println("document ids found in '" + args[0] + "':");
        for (String docid : d.getDocuments().keySet())
            System.out.println("\t" + docid);
    }

}
