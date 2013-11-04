package healthSurveillanceFramework.fileFormats;

import java.util.ArrayList;
import java.util.Map;

public class DocFiles extends JsonFile {
    private String[] filenames;

    @SuppressWarnings("unchecked")
    public void loadJson(String filename) {
        String json = readFile(filename);
        Map<String, ArrayList<String>> data = (Map<String, ArrayList<String>>) parser.parseJson(json);
        filenames = data.get("root").toArray(new String[0]);
    }

    public void writeJson(String filename) {
        String json = generator.generateJson(filenames);

        // quick-json encloses the data in an outside array
        // TODO figure out a better way to handle this
        json = json.substring(1, json.length() - 1);

        writeFile(json, filename);
    }

    public String[] getFilenames() {
        return filenames;
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("usage: <DocumentFiles file>");
            System.exit(1);
        }

        DocFiles df = new DocFiles();
        df.loadJson(args[0]);

        System.out.println("files found in '" + args[0] + "':");
        for (String f : df.getFilenames())
            System.out.println("\t" + f);
    }

}

