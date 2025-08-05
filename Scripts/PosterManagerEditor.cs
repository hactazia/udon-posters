#if UNITY_EDITOR
using System.Linq;
using UnityEditor;
using UnityEngine;
using VRC.SDKBase;

namespace Hactazia.Posters {
	public static class PosterManagerEditor {
		internal const string BaseUrl       = "http://localhost:8000/";
		internal const int    AtlasCount    = 128;
		private const  double CheckInterval = 1.0;

		private static double _lastCheckTime;

		private static PosterManager Manager
			=> Object.FindObjectOfType<PosterManager>();

		private static Poster[] Posters
			=> Object.FindObjectsOfType<Poster>();

		private static bool UpdatePosters(PosterManager manager) {
			var findPosters = Posters;
			var crtPosters  = manager.posters;
			if (findPosters.Length == crtPosters.Length && !findPosters.Where((t, i) => i >= crtPosters.Length || t != crtPosters[i]).Any())
				return false;
			manager.posters = findPosters;
			return true;
		}

		private static bool UpdateUrls(PosterManager manager) {
			var dirty = false;

			if (string.IsNullOrEmpty(manager.baseUrl)) {
				manager.baseUrl = BaseUrl;
				dirty           = true;
			}

			if (manager.atlasCount < 1) {
				manager.atlasCount = AtlasCount;
				dirty              = true;
			}

			var metaUrl = $"{manager.baseUrl.TrimEnd('/')}/atlas.json";
			if (!dirty && manager.metaUrl.Get() == metaUrl) return false;
			manager.metaUrl   = new VRCUrl(metaUrl);
			manager.atlasUrls = new VRCUrl[manager.atlasCount];
			for (var i = 0; i < manager.atlasUrls.Length; i++)
				manager.atlasUrls[i] = new VRCUrl($"{manager.baseUrl.TrimEnd('/')}/atlas/{i}.png");

			return true;
		}

		private static bool UpdateMaterial(PosterManager manager) {
			if (manager.material) return false;
			var material = Resources.Load<Material>("PosterManagerMaterial");
			if (!material) return false;
			manager.material = material;
			return true;
		}

		private static void OnEditorUpdate() {
			if (Application.isPlaying) return;
			if (EditorApplication.timeSinceStartup - _lastCheckTime < CheckInterval) return;
			_lastCheckTime = EditorApplication.timeSinceStartup;
			CheckManagerDirty();
		}

		private static void CheckManagerDirty() {
			var manager = Manager;
			if (!manager) return;
			if (!UpdatePosters(manager) && !UpdateUrls(manager) && !UpdateMaterial(manager)) return;
			EditorUtility.SetDirty(manager);
			AssetDatabase.SaveAssets();
		}

		[InitializeOnLoadMethod]
		public static void Initialize()
			=> EditorApplication.update += OnEditorUpdate;
	}
}
#endif